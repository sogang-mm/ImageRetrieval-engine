from rest_framework import serializers
from Engine.models import *


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryModel
        fields = (
        'image', 'feature', 'dataset', 'extractor', 'topk', 'extract_time', 'search_time', 'results', 'uploaded_date',
        'updated_date')
        read_only_fields = ('extract_time', 'search_time', 'uploaded_date', 'updated_date', 'results')

    def to_representation(self, instance):
        _repr = super(QuerySerializer, self).to_representation(instance)
        _repr.update({'dataset': instance.dataset.name,
                      'extractor': instance.extractor.name})
        return _repr
