from collections import defaultdict
import torch
import numpy as np
import os
from Module.sequential.engine import FlatL2Engine


class SearchEngine:
    def __init__(self, features):
        self.images = dict()
        self.engine = defaultdict(dict)
        self.device = os.environ['NVIDIA_USED_DEVICE_ID']

        for dataset, feat in features.items():
            for extractor, v in feat.items():
                print(f'[Load Feature] {dataset} {extractor}')
                self.images[dataset] = np.load(v['images'])
                self.engine[dataset][extractor] = FlatL2Engine(np.concatenate([self.load(p) for p in v['path']]), self.device)
                print(f'[Load Feature] {dataset} {extractor} ... {self.images[dataset].shape}')

    def search_by_path(self, feature_path, dataset, extractor, topk):
        query_feature = self.load(feature_path)
        engine = self.engine[dataset][extractor]
        (dist, indice),search_time = engine.search(query_feature, topk)
        result = [{'rank': n, 'distance': float(i[1]), 'image': self.images[dataset][i[0]]} for
                  n, i in enumerate(zip(indice[0], dist[0]), start=1)]
        return result,search_time

    def load(self, p):
        _, ext = os.path.splitext(p)
        if ext in ['.pth', '.pt']:
            f = torch.load(p).cpu().numpy()
        elif ext in ['.npy']:
            f = np.load(p)
        return f
