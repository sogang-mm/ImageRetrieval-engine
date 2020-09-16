from __future__ import print_function
from collections import defaultdict
from RetrievalEngine.celerys import app
from celery.signals import worker_init, worker_process_init
from billiard import current_process
from datetime import datetime, timedelta

import requests
import json
import csv
import os
from urllib.request import urlretrieve

from RetrievalEngine.settings import ENGINE, MEDIA_ROOT


@worker_init.connect
def model_load_info(**__):
    print("====================")
    print("Worker RetrievalExtractor Initialize")
    print("====================")


@worker_process_init.connect
def module_load_init(**__):
    global engine
    worker_index = current_process().index

    print("====================")
    print(" Worker Id: {0}".format(worker_index))
    print("====================")

    from Manager.models import DatasetModel, ExtractorModel, FeatureModel
    datasets = DatasetModel.objects.filter(engine__name=ENGINE)
    extractors = ExtractorModel.objects.filter(feature__dataset__engine__name=ENGINE)

    features = defaultdict(dict)
    for d in datasets:
        for e in extractors:
            f = FeatureModel.objects.filter(dataset=d, extractor=e)
            if f.count() != 0:
                features[d.name][e.name] = {'path': [p.path for p in f.order_by('idx')],
                                            'images': d.images}

    from Module.main import SearchEngine
    engine = SearchEngine(features)


def time_to_seconds(time):
    return sum([60**(2 - n) * float(i) for n, i in enumerate(time.split(":"))])


@app.task
def send_request_to_extractor(image_path, save_to, extractor_url):    
    response = requests.post(url=extractor_url, data=dict(),
                             files={'image': open(image_path, 'rb')})
    if response.status_code != 201:
        return False
    _response = json.loads(response.text)
    feature = _response['feature']
    name, _ = urlretrieve(feature, save_to)
    feature = os.path.relpath(save_to, MEDIA_ROOT)
    extract_time = time_to_seconds(_response.get('extract_time'))

    print("extract time: ", timedelta(seconds=extract_time))
    return feature, extract_time


@app.task
def search_by_path(feature_path, dataset, extractor, topk, save_to):
    result, search_time = engine.search_by_path(feature_path, dataset, extractor, topk)
    print("search time: ", timedelta(seconds=search_time))

    start = datetime.now()
    with open(save_to, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=result[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(result)
    result = os.path.relpath(save_to, MEDIA_ROOT)
    print("save time: {}".format(datetime.now() - start))
    return result, search_time
