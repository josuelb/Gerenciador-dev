from django.db import models
import uuid


class Tecnologias(models.Model):
    id = models.UUIDField(
        unique=True,
        auto_created=True,
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    nome = models.CharField(max_length=100)


class Programador(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        auto_created=True, 
        unique=True, 
        default=uuid.uuid4,
        editable=False
    ) 
    nome = models.CharField(max_length=100)
    tecnologias = models.ManyToManyField(Tecnologias, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome}, Tecnologia: {self.tecnologias}"


class Projetos(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        auto_created=True, 
        unique=True, 
        default=uuid.uuid4,
        editable=False
    ) 
    nome = models.CharField(max_length=100)
    datainicio = models.DateField()
    datafim = models.DateField()
    tecnologias = models.ManyToManyField(Tecnologias, on_delete=models.CASCADE)

    def __str__(self):
        return f"Projeto:{self.nome}, Tecnologias: {self.tecnologias}"


class Alocacoes(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        auto_created=True, 
        unique=True, 
        default=uuid.uuid4,
        editable=False
    ) 
    projetos = models.ManyToManyField(Projetos, on_delete=models.CASCADE)
    desenvolvedor = models.ForeignKey(Programador, on_delete=models.CASCADE)
    horas = models.TimeField()

    def __str__(self):
        return f"""
        Projetos: {self.projetos};
        Desenvolvedor: {self.desenvolvedor};
        Horas: {self.horas}
        """
