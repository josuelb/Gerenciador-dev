from rest_framework.routers import DefaultRouter

from .views import (
    AlocacoesView,
    ProgramadorView,
    ProjetoView,
    TecnologiasView,
    UserCreateView
)

router = DefaultRouter()
router.register(prefix=r'alocacoes', viewset=AlocacoesView, basename='alocar')
router.register(r'programa', viewset=ProgramadorView, basename='programador')
router.register(r'projetos', viewset=ProjetoView, basename='projetos')
router.register(r'tecno', viewset=TecnologiasView, basename='tecnologias')
router.register(r'register', viewset=UserCreateView, basename='Registrar')
