from rest_framework import serializers
from .models import ShareData

class ShareDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareData
        fields = '__all__'