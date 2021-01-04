from .models import Data
from rest_framework import serializers

class DataSerializers(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'

class DataSerializers0(serializers.Serializer):

    name = serializers.CharField(max_length=30)
    age = serializers.IntegerField()
    city = serializers.CharField(max_length=30)
    occupation = serializers.CharField(max_length=30)
    id = serializers.IntegerField()

class DataSerializers1(serializers.Serializer):

    name = serializers.CharField(max_length=30)
    age = serializers.IntegerField()
    city = serializers.CharField(max_length=30)
    occupation = serializers.CharField(max_length=30)
    # id = serializers.IntegerField()

    def create(self, validated_data):
        return Data.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.city = validated_data.get('city', instance.city)
        instance.occupation = validated_data.get('occupation', instance.occupation)

        instance.save()
        return instance