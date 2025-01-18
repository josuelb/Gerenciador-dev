import datetime
from http import HTTPStatus
import json
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User  

from apps.gerenciaDev.models import (
    Programador,
    Projetos, 
    Tecnologias
)

class ProjetosViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        
        self.tecnologia = Tecnologias.objects.create(nome='TestTecn')
        self.programador = Programador.objects.create(nome='TestProgram')
        self.programador.tecnologias.add(self.tecnologia)
        self.id_current = None
        self.projeto = Projetos.objects.create( 
            nome='Testproject', horas=datetime.time(0,10).isoformat(),
            datainicio=timezone.now().date(), 
            datafim=(timezone.now() + timezone.timedelta(days=30)).date() 
        )

        self.token = RefreshToken.for_user(self.user).access_token
    
    def test_criacao_projeto_OK(self):
        dtinicio=timezone.now().date().isoformat()
        dtfim=(timezone.now() + timezone.timedelta(days=30)).date().isoformat()

        data = {
            'nome': 'ProjetoCriado',
            'datainicio': dtinicio,
            'datafim': dtfim,
            'horas': datetime.time(0,10).isoformat(),
            'tecnologias': [str(self.tecnologia.id)]
        }
        response = self.client.post(
            '/api/projetos/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'  
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(
            Projetos.objects.filter(id=response.data.get('id')).exists()
        )
    
    def test_deletar_projeto_OK(self):
        data = {'id': str(self.projeto.id)}
        response = self.client.delete(
            '/api/projetos/apagarProjeto/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'  
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Projetos.objects.filter(id=self.projeto.id).exists())
