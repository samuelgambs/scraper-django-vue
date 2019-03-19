from main.models import Cursos
from rest_framework import serializers


class CursosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cursos
        fields = '__all__'