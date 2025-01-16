from rest_framework import viewsets
from rest_framework.decorators import action

from gerenciaDev import serializer
from gerenciaDev import models

class ProgramadorView(viewsets.ModelViewSet):
    serializer_class = serializer.ProgramadorSerializer
    queryset = models.Programador.objects.all()


class ProjetoView(viewsets.ModelViewSet):
    serializer_class = serializer.ProjetoSerializer
    queryset = models.Projetos.objects.all()


class AlocacoesView(viewsets.ModelViewSet):
    serializer_class = serializer.AlocacoeSerializer
    queryset = models.Alocacoes.objects.all()


class TecnologiasView(viewsets.ModelViewSet):
    serializer_class = serializer.TecnologiaSerializer
    queryset = models.Tecnologias.objects.all()

