from rest_framework import serializers
from kitablar.models import Kitab, Yorum


class YorumSerializers(serializers.ModelSerializer):
    yorum_sahibi = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Yorum
        # fields = '__all__'
        exclude = ['kitab']

class KitabSerializers(serializers.ModelSerializer):
    yorumlar = YorumSerializers(many=True, read_only=True)
    
    class Meta:
        model = Kitab
        fields = '__all__'


