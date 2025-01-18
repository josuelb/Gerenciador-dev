from rest_framework import serializers
from django.contrib.auth.models import User

from . import models

class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User 
        fields = ['username', 'password', 'email'] 
        def create(self, validated_data): 
            user = User.objects.create_user( 
                username=validated_data['username'], 
                email=validated_data['email'], 
                password=validated_data['password'] 
            ) 
            return user
    

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