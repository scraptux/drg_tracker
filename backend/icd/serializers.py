from rest_framework import serializers
from .models import Version, Kapitel, Gruppen, Kodes

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'

class KapitelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kapitel
        fields = '__all__'

class GruppenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gruppen
        fields = '__all__'

class KodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kodes
        fields = '__all__'