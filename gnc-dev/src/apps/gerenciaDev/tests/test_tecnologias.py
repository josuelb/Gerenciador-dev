import json
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from http import HTTPStatus
from django.contrib.auth.models import User  

from apps.gerenciaDev.models import (
    Projetos,
    Tecnologias
)

class TecnologiasViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='password')
        
        self.tecnologia = Tecnologias.objects.create(nome='TestTecn')
        self.projeto = Projetos.objects.create( 
            nome='Testproject', horas='10:00:00',
            datainicio=timezone.now().date(), 
            datafim=(timezone.now() + timezone.timedelta(days=30)).date() 
        )

        self.token = RefreshToken.for_user(self.user).access_token
    
    def test_criar_tecnologia_OK(self):
        response = self.client.post(
            '/api/tecno/',
            data=json.dumps({'nome': 'TecnoTestCase'}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'  
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(
            Tecnologias.objects.filter(id=response.data.get('id')).exists()
        )

    def test_deletar_tecnologia_OK(self):
        data = {'id': str(self.tecnologia.id)}
        response = self.client.delete(
            '/api/tecno/apagarTecnologia/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}' 
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(
            Tecnologias.objects.filter(id=self.tecnologia.id).exists()
        )
