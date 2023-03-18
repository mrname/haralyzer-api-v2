from haralyzer import HarParser
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
        fields = ('name', 'created', 'url', 'result')

    def create(self, validated_data):
        obj = Scan.objects.create(**validated_data)
        # TODO - Consider making it async by kicking this off in a background
        # task. In such a case, it could potentially even be triggered by model
        # signals instead of here in the serializer.
        results = create_har_data(obj.url)
        har_parser = HarParser(results)

        # Since we always produce the HAR from a single URL, we can blindly
        # assume that we will always only have one page. As a result, we can
        # pull things like load times from the page
        assert len(har_parser.pages) == 1
        page = har_parser.pages[0]

        # Start off with a few oddball attrs whose names do not match
        scan_result_details = {
            # A bit of a hack, we SHOULD be able to use page_load_time property
            # but it does not like the HAR we are producing
            #'total_load_time': len(har_parser.create_asset_timeline(page.entries)),
            'total_load_time': 0,
            'total_size': page.page_size
        }

        # The rest can be mapped directly
        for attr_name in ScanResult._haralyzer_defined_attrs:
            scan_result_details[attr_name] = getattr(page, attr_name)

        scan_result_obj = ScanResult.objects.create(scan=obj, raw_results=results, **scan_result_details)

        return obj
