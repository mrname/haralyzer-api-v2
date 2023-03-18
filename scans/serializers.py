from rest_framework import serializers

from .controllers.har import create_har_data
from .models import Scan, ScanResult

class ScanResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanResult
        fields = '__all__'

class ScanSerializer(serializers.ModelSerializer):
    result = ScanResultSerializer(read_only=True)

    class Meta:
        model = Scan
        #fields = '__all__'
        fields = ('name', 'created', 'url', 'result')

    def create(self, validated_data):
        obj = Scan.objects.create(**validated_data)
        # TODO - Consider making it async by kicking this off in a background
        # task. In such a case, it could potentially even be triggered by model
        # signals instead of here in the serializer.
        results = create_har_data(obj.url)
        scan_result_obj = ScanResult.objects.create(scan=obj, raw_results=results)
        return obj
