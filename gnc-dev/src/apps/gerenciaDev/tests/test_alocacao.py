import datetime
import json
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from http import HTTPStatus

from apps.gerenciaDev.models import (
    Programador,
    Projetos,
    Tecnologias,
    Alocacoes
)

class AlocacoesViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='password')
        self.tecnologia = Tecnologias.objects.create(nome='TestTecn')
        self.programador = Programador.objects.create(nome='TestProgram')
        self.programador.tecnologias.add(self.tecnologia)
        self.projeto = Projetos.objects.create(
            nome='Testproject', 
            horas=datetime.time(10,00).isoformat(),
            datainicio=timezone.now().date().isoformat(),
            datafim=(timezone.now() + timezone.timedelta(days=30)).date().isoformat()
        )
        self.projeto.tecnologias.add(self.tecnologia)
        self.token = RefreshToken.for_user(self.user).access_token

    def test_alocar_programador_OK(self):
        data = {
            'programador_id': str(self.programador.id),
            'projeto_id': str(self.projeto.id),
            'horas_planejadas': datetime.time(5,00).isoformat(),
            'data_alocacao': timezone.now().date().isoformat()
        }
        response = self.client.post(
            f'/api/alocacoes/alocar/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(
            Alocacoes.objects.filter(
                id=response.data.get('id')
            ).exists()
        )

    def test_apagar_alocacao_OK(self):                
        self.alocacao = Alocacoes.objects.create(
            desenvolvedor = self.programador,
            horas=datetime.time(5,00).isoformat()
        )
        self.alocacao.projetos.add(self.projeto)
        self.alocacao.save()

        data = {'id': str(self.alocacao.id)}
        response = self.client.delete(
            '/api/alocacoes/apagarAlocacao/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Alocacoes.objects.filter(id=self.alocacao.id).exists())
