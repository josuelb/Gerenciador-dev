from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from http import HTTPStatus

from apps.gerenciaDev.models import (
    Alocacoes,
    Programador, 
    Projetos,
    Tecnologias
)


class ProgramadorViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', email='test@test.com')
        
        self.tecnologia = Tecnologias.objects.create(nome='TestTecn')
        self.programador = Programador.objects.create(nome='TestProgram')
        self.programador.tecnologias.add(self.tecnologia)
        self.projeto = Projetos.objects.create( 
            nome='Testproject', horas='10:00:00',
            datainicio=timezone.now().date(), 
            datafim=(timezone.now() + timezone.timedelta(days=30)).date() 
        )

        self.token = RefreshToken.for_user(self.user).access_token
    
    def test_criar_novo_programador_OK(self):
        data = {
            'nome': 'testprogramador',
            'tecnologias': [self.tecnologia.id]
        }
        response = self.client.post(
            '/api/programa/',
            data=data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'  
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.data['nome'], 'testprogramador')

    def test_deletar_programador_OK(self):
        response = self.client.delete(
            '/api/programa/apagarProgramador/',
            data={'id': self.programador.id},
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'  
        )

        self.assertEqual(response.data['status'], 'O programador foi deletado')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(
            Programador.objects.filter(id=self.programador.id).exists()
        )
