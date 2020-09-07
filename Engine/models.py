from django.db import models
from Engine.utils import filename
from Engine.tasks import *
import os
from RetrievalEngine import settings
from Manager.models import *
from datetime import timedelta


class QueryModel(models.Model):
    image = models.ImageField(upload_to=filename.uploaded_date, null=True)
    feature = models.FileField(upload_to=filename.uploaded_date, null=True)
    dataset = models.ForeignKey(DatasetModel, on_delete=models.DO_NOTHING, db_constraint=False)
    extractor = models.ForeignKey(ExtractorModel, on_delete=models.DO_NOTHING, db_constraint=False)
    topk = models.IntegerField(default=100)
    results = models.FileField(upload_to=filename.uploaded_date)
    extract_time = models.DurationField(default=timedelta(days=0, hours=0))
    search_time = models.DurationField(default=timedelta(days=0, hours=0))
    uploaded_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(QueryModel, self).save(*args, **kwargs)
        if not bool(self.feature):
            feature, extract_time = send_request_to_extractor.delay(self.image.path,
                                                                    f'{self.image.path}.pth',
                                                                    self.extractor.module_url).get()
            if not feature:
                raise exceptions.ValidationError('Cannot extract feature. Check Extractor module')
            self.feature = feature
            self.extract_time = timedelta(seconds=extract_time)

        self.results, search_time = search_by_path.delay(self.feature.path,
                                                              self.dataset.name,
                                                              self.extractor.name,
                                                              self.topk,
                                                              f'{self.image.path}.csv').get()
        self.search_time=timedelta(seconds=search_time)
        print(self.results)

        super().save()
