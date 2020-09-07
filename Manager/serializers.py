from rest_framework import serializers
from Manager.models import *


class ExtractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractorModel
        fields = ('name', 'url', 'module_url', 'type', 'engine', 'status')
        read_only_fields = ('url', 'type', 'status',)

    def to_representation(self, instance):
        _repr = super(ExtractorSerializer, self).to_representation(instance)
        _repr.update({'engine': instance.engine.name})
        return _repr


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetModel
        fields = ('url', 'name', 'path', 'images', 'count', 'engine')
        read_only_fields = ('name',)

    def to_representation(self, instance):
        _repr = super(DatasetSerializer, self).to_representation(instance)
        _repr.update({'engine': instance.engine.name})
        return _repr


class EngineSerializer(serializers.ModelSerializer):
    dataset = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    extractor = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = EngineModel
        fields = ('name', 'url', 'module_url', 'type', 'status', 'dataset', 'extractor',)
        read_only_fields = ('url', 'type', 'status', 'dataset', 'extractor',)


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureModel
        fields = ('dataset', 'extractor', 'idx', 'path')
        read_only_fields = ('dataset', 'extractor', 'idx')


    def to_representation(self, instance):
        _repr = super(FeatureSerializer, self).to_representation(instance)
        _repr.update({'dataset': instance.dataset.name,
                      'extractor': instance.extractor.name})
        return _repr