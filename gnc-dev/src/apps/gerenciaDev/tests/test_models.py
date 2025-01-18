import datetime
from rest_framework.test import APITestCase
from django.utils import timezone

from apps.gerenciaDev.models import (
    Alocacoes,
    Programador,
    Projetos,
    Tecnologias
)

class ModelsTestCase(APITestCase):
    def setUp(self):
        self.tecn = Tecnologias(nome='TestCriacao')
        self.tecn.save()

        self.programador_current = Programador(nome='TestProgramador')
        self.programador_current.save()
        self.programador_current.tecnologias.add(self.tecn)

        self.projeto_current = Projetos(
            nome='Testproject', 
            horas='10:00:00',
            datainicio=timezone.now().date(), 
            datafim=(timezone.now() + timezone.timedelta(days=30)).date()        
        )
        self.projeto_current.save()
        self.projeto_current.tecnologias.add(self.tecn)

        self.alocacao_current = Alocacoes(
            horas=datetime.time(0, 10),
            desenvolvedor=self.programador_current
        )
        self.alocacao_current.save()
        self.alocacao_current.projetos.add(self.projeto_current)
        
    def test_criacao_tecnologia(self):
        tecnologias = Tecnologias.objects.get(nome="TestCriacao")
        self.assertEqual(tecnologias.nome, self.tecn.nome)
    
    def test_criacao_programador(self):
        programador = Programador.objects.get(nome='TestProgramador')
        self.assertEqual(programador.nome, self.programador_current.nome)
        self.assertEqual(programador.tecnologias, self.programador_current.tecnologias)
    
    def test_criacao_projeto(self):
        projetos = Projetos.objects.get(nome='Testproject')
        self.assertEqual(projetos.nome, self.projeto_current.nome)
        self.assertEqual(projetos.datainicio, self.projeto_current.datainicio)
        self.assertEqual(projetos.datafim, self.projeto_current.datafim)
        self.assertEqual(projetos.tecnologias, self.projeto_current.tecnologias)

    def test_criacao_alocacao(self):
        alocacao = Alocacoes.objects.get(projetos=self.projeto_current)
        self.assertEqual(alocacao.projetos, self.alocacao_current.projetos)
        self.assertEqual(alocacao.desenvolvedor, self.alocacao_current.desenvolvedor)
        self.assertEqual(alocacao.horas, self.alocacao_current.horas)
