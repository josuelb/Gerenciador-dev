from django.utils.dateparse import parse_datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from http import HTTPStatus

from . import serializer
from . import models

class ProgramadorView(viewsets.ModelViewSet):
    serializer_class = serializer.ProgramadorSerializer
    queryset = models.Programador.objects.all()


class ProjetoView(viewsets.ModelViewSet):
    serializer_class = serializer.ProjetoSerializer
    queryset = models.Projetos.objects.all()


class AlocacoesView(viewsets.ModelViewSet):
    serializer_class = serializer.AlocacoeSerializer
    queryset = models.Alocacoes.objects.all()

    @action(detail=True, methods=['post'])
    def alocar(self, request, pk=None):
        projeto_id = pk
        programador_id = request.data.get('programador_id')

        try:
            programador = models.Programador.objects.get(id=programador_id)
            projeto = models.Projetos.objects.get(id=projeto_id)
            horas_planejadas = request.data.get('horas_planejadas') 
            data_alocacao = request.data.get('data_alocacao')

            tecnologias_programador = programador.tecnologias.all()
            tecnologias_projeto = projeto.tecnologias.all()

            tecnologias_comuns = tecnologias_programador & tecnologias_projeto

            if not tecnologias_comuns.exists():
                return Response(
                    {'error': 'O programador não tem tecnologias cadastradas!'},
                    status=HTTPStatus.FORBIDDEN
                )
            
            data_inicial = parse_datetime(projeto.datainicio) 
            data_final = parse_datetime(projeto.datafim) 
            data_alocacao = parse_datetime(data_alocacao) 
            if data_alocacao < data_inicial or data_alocacao > data_final: 
                return Response(
                    {'error': 'A data de alocação deve estar dentro do intervalo do projeto'},
                    status=HTTPStatus.NOT_FOUND
                ),

            horas_alocadas = sum(alocacao.horas for alocacao in projeto.alocacoes_set.all()) 
            if horas_alocadas + horas_planejadas > projeto.horas: 
                return Response(
                    {'error': 'As horas planejadas para o projeto serão excedidas com essa alocação'}, 
                    status=HTTPStatus.BAD_REQUEST
                )

            alocacao, created = models.Alocacoes.objects.get_or_create( 
                programador=programador, 
                projeto=projeto,
                defaults={'horas': horas_planejadas,} 
            )
            if created:
                return Response({'status': HTTPStatus.CREATED})
            else:
                return Response(
                    {'status': 'Programador já alocado neste Projeto!'},
                    status=HTTPStatus.ACCEPTED
                )
        except models.Programador.DoesNotExist: 
            return Response(
                {'error': 'Programador não encontrado'}, 
                status=HTTPStatus.NOT_FOUND)
        except models.Programador.DoesNotExist: 
            return Response(
                {'error': 'Projeto não encontrado'}, 
                status=HTTPStatus.NOT_FOUND)


class TecnologiasView(viewsets.ModelViewSet):
    serializer_class = serializer.TecnologiaSerializer
    queryset = models.Tecnologias.objects.all()

