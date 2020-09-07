from django.db import models
from rest_framework import exceptions
import requests
import os
import numpy as np
from RetrievalEngine import settings
from django.urls import reverse
from rest_framework import reverse


class EngineModel(models.Model):
    name = models.CharField(max_length=32)
    module_url = models.URLField()
    type = models.CharField(max_length=16, default='engine')
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'module_url')

    def save(self, *args, **kwargs):
        self.check_status()
        super(EngineModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def check_status(self):
        try:
            response = requests.get(self.module_url)
            self.status = response.ok
        except:
            self.status = False
            # raise exceptions.ValidationError('Cannot access URL. Check module URL.')


class ExtractorModel(models.Model):
    name = models.CharField(max_length=32)
    module_url = models.URLField()
    type = models.CharField(max_length=16, default='extractor')
    engine = models.ForeignKey(EngineModel, on_delete=models.DO_NOTHING, related_name='extractor', null=True)
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'module_url', 'engine')

    def save(self, *args, **kwargs):
        self.check_status()
        # kwargs['using'] = settings.MANAGER_DB
        super(ExtractorModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def check_status(self):
        try:
            response = requests.get(self.module_url)
            self.status = response.ok
        except:
            self.status = False
            # raise exceptions.ValidationError('Cannot access URL. Check module URL.')


class DatasetModel(models.Model):
    name = models.CharField(max_length=32)
    path = models.FilePathField(path='/dataset/images',
                                allow_files=False, allow_folders=True, recursive=False)
    count = models.IntegerField(default=0)
    images = models.FilePathField(path='/dataset/images',
                                  allow_files=True, allow_folders=False, recursive=False)
    engine = models.ForeignKey(EngineModel, on_delete=models.DO_NOTHING, related_name='dataset', null=True)

    class Meta:
        unique_together = ('path', 'engine')

    def save(self, *args, **kwargs):
        self.name = os.path.basename(self.path)
        if self.images is None:
            default_image_list = f'{self.path}-list.npy'
            if os.path.exists(default_image_list):
                self.images =default_image_list
            else:
                self.images=f'{self.path}-auto-list.npy'
                image_list = [os.path.join(base, f) for base, folder, files in os.walk(self.path) for f in files]
                np.save(self.images, np.array(image_list))
        self.count = len(np.load(self.images))

        super(DatasetModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class FeatureModel(models.Model):
    dataset = models.ForeignKey(DatasetModel, on_delete=models.DO_NOTHING)
    extractor = models.ForeignKey(ExtractorModel, on_delete=models.DO_NOTHING)
    idx = models.IntegerField(default=0)
    path = models.FilePathField(path='/dataset/features',
                                allow_files=True, allow_folders=False, recursive=False, unique=True)

    def save(self, *args, **kwargs):
        # self.path => {dataset}-{extractor}-{idx}
        dataset, extractor, idx = os.path.splitext(os.path.basename(self.path))[0].split('-')
        self.dataset = DatasetModel.objects.get(name=dataset)
        self.extractor = ExtractorModel.objects.get(name=extractor)
        self.idx = idx
        # kwargs['using'] = settings.MANAGER_DB
        super(FeatureModel, self).save(*args, **kwargs, )

    def __str__(self):
        return self.path
