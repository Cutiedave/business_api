from rest_framework import serializers
from .models import Business_case_data, Lead
class MepSerializer(serializers.ModelSerializer):
    class Meta:
        #image_url = serializers.SerializerMethodField('get_image_url')
        model = Business_case_data
        fields = "__all__"
        # def get_image_url(self, obj):
        #     return obj.image.url

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        #image_url = serializers.SerializerMethodField('get_image_url')
        model = Lead
        fields = "__all__"
        # def get_image_url(self, obj):
        #     return obj.image.url