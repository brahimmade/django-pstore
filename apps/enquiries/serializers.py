from rest_framework import serializers

from .models import Enquiry


# Create your tests here.
class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = "__all__"
