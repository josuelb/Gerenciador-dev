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

    @action(detail=False, methods=['delete'])
    def apagarProgramador(self, request):
        id_programaddor = request.data.get('id')
        if not id_programaddor:
            return Response(
                {'status': 'Não foi passado o id'},
                status=HTTPStatus.BAD_REQUEST
            )

        try:
            programador = models.Programador.objects.get(id=id_programaddor) 
            programador.delete()
            
            return Response(
                {'status': 'O programador foi deletado'},
                status=HTTPStatus.OK
            )
        except models.Programador.DoesNotExist as error:
            return Response(
                {'status': 'O programador não encontrado'},
                status=error
            )


class ProjetoView(viewsets.ModelViewSet):
    serializer_class = serializer.ProjetoSerializer
    queryset = models.Projetos.objects.all()

    @action(detail=False, methods=['delete'])
    def apagarProjeto(self, request):
        id_current = request.data.get('id')
        if not id_current:
            return Response(
                {'status': 'O Id não foi passado!'},
                status=HTTPStatus.BAD_REQUEST
            )
        
        try:
            projetos_db = models.Projetos.objects.get(id=id_current)
            projetos_db.delete()
            return Response(
                {'status': 'Projeto deletado'},
                status=HTTPStatus.OK
            )
        except models.Projetos.DoesNotExist as error:
            return Response(
                {'status': 'O projeto não está cadastrado!'},
                status=error
            )

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
        except models.Programador.DoesNotExist as error: 
            return Response(
                {'error': 'Programador não encontrado'}, 
                status=error
            )
        except models.Projetos.DoesNotExist as error: 
            return Response(
                {'error': 'Projeto não encontrado'}, 
                status=error
            )
        
    @action(detail=True, methods=['delete'])
    def apagarAlocacao(self, request, pk=None):
        if not request.data['id']:
            return Response(
                {'status': 'Não foi passado o id'},
                status=HTTPStatus.BAD_REQUEST
            )
        alocacao_db = models.Alocacoes.objects.get(id=request.data['id'])

        try:
            alocacao_db.delete()
            return Response(
                {'status':'Alocação deletada!'},
                status=HTTPStatus.OK
            )
        except models.Alocacoes.DoesNotExist as error:
            return Response(
                {'status': 'Alocação não existente'},
                status=error
            )


class TecnologiasView(viewsets.ModelViewSet):
    serializer_class = serializer.TecnologiaSerializer
    queryset = models.Tecnologias.objects.all()

    @action(detail=False, methods=['delete'])
    def apagarTecnologia(self, request):
        id_current = request.data.get('id')
        if not id_current:
            return Response(
                {'status': 'O Id da tecnologia não foi passado'},
                status=HTTPStatus.BAD_REQUEST
            )

        try: 
            tecnologia_db = models.Tecnologias.objects.get(id=id_current)
            tecnologia_db.delete()
            return Response(
                {'status': 'Tecnologia deletada'},
                status=HTTPStatus.OK
            )
        except models.Tecnologias.DoesNotExist as error:
            return Response(
                {'status': 'Tecnologia não encontrada ou nao existente'},
                status=error
            )

