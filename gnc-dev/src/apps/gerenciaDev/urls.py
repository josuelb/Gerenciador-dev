from django.urls import path

from views import (
    AlocacoesView,
    ProgramadorView,
    ProjetoView,
    TecnologiasView
)


urlpatterns = [
    path('aloca/', AlocacoesView.as_view(), name="Alocações"),
    path('program/', ProgramadorView.as_view(), name="Programador"),
    path('projetos/', ProjetoView.as_view(), name="Projetos"),
    path('Tecno/', TecnologiasView.as_view(), name="Tecnologias")
]