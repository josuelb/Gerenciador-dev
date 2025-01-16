from rest_framework import serializers

from gerenciaDev import models


class ProgramadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Programador
        fields = "__all__"
    

class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Projetos
        fields = "__all__"


class AlocacoeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Alocacoes
        fields = "__all__"


class TecnologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tecnologias
        fields = "__all__"