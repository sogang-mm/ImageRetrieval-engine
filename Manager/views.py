from django.shortcuts import render
from Manager.models import *
from Manager.serializers import *
from rest_framework import viewsets
from RetrievalEngine.settings import ENGINE
import os


class ExtractorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExtractorModel.objects.filter(feature__dataset__engine__name=ENGINE)
    serializer_class = ExtractorSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.order_by('-id')

        token = self.request.query_params.get('id', None)
        if token is not None:
            queryset = queryset.filter(token=token)

        return queryset


class EngineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EngineModel.objects.filter(name=ENGINE)
    serializer_class = EngineSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.order_by('-id')

        token = self.request.query_params.get('id', None)
        if token is not None:
            queryset = queryset.filter(token=token)

        return queryset


class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DatasetModel.objects.filter(engine__name=ENGINE)
    serializer_class = DatasetSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.order_by('-id')

        token = self.request.query_params.get('id', None)
        if token is not None:
            queryset = queryset.filter(token=token)

        return queryset


class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeatureModel.objects.filter(dataset__engine__name=ENGINE)
    serializer_class = FeatureSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.order_by('-id')

        token = self.request.query_params.get('id', None)
        if token is not None:
            queryset = queryset.filter(token=token)

        return queryset
