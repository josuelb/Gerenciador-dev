from django.contrib import admin

from models import (
    Alocacoes,
    Programador,
    Projetos, 
    Tecnologias
)

# Register your models here.

admin.register(Alocacoes)
admin.register(Programador)
admin.register(Projetos)
admin.register(Tecnologias)