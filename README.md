# Gerenciador-dev

## Descrição

Esse Projeto é um gerenciador de desenvolvedores pra projetos ou atividades,
pensado de forma segura, ele aloca hora e tecnologia que será usada no projeto.

## Status do projeto 

Atualmente (data que foi postado o readme), parei o desenvolvimento por está 
em uma versão estável.

## Estrutura do projeto 

```plaintext
├── Gerenciador-dev
|   ├── .venv
|   ├── gnc-dev
│   │   ├── src
│   │   |   ├── apps
│   │   │   │   ├── gerenciaDev
│   │   │   │   │   ├── tests
│   │   │   │   │   │   ├── test_alocacao.py
│   │   │   │   │   │   ├── test_models.py
│   │   │   │   │   │   ├── test_programador.py
│   │   │   │   │   │   ├── test_projetos.py
│   │   │   │   │   │   └── test_tecnologias.py
│   │   │   │   │   ├── admin.py
│   │   │   │   │   ├── apps.py
│   │   │   │   │   ├── models.py
│   │   │   │   │   ├── serializer.py
│   │   │   │   │   ├── urls.py
│   │   │   │   │   └── views.py
│   │   ├── gnc_dev
│   │   │   ├── asgi.py
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   └── wsgi.py
|   │   └── manage.py
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── .gitattributes
│   ├── .gitignore 
```

## Tecnologias usadas 

Usei o **poetry** pra gerenciar todas as bibiotecas e ferramentas usadas:

```.toml
[project]
name = "gerenciador-dev"
version = "0.1.0"
description = ""
authors = [
    {name = "Josué Luiz Barbosa e Silva",email = "104951932+josuelb@users.noreply.github.com"}
]
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "django (>=5.1.5,<6.0.0)",
    "djangorestframework (>=3.15.2,<4.0.0)",
    "djangorestframework-simplejwt[crypto] (>=5.4.0,<6.0.0)",
    "psycopg2-binary (>=2.9.10,<3.0.0)",
    "psycopg2 (>=2.9.10,<3.0.0)",
]


[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

## API screen

A url deve ir ate o ***/api*** onde está mostrando todas as urls.
![Img urls]

#### Campo de Login 

![Img authenticação](https://github.com/josuelb/Gerenciador_Books/blob/9faf2ec526389418c0bf08b7ee7905d49f1df294/imgs_readme/start_docs_3.png)

## Passos pra startar a api

### Inicializar o redis e o banco de dados  

O banco de dados e o cache devem ser iniciados antes de tudo.

No windows usa-se o comando para iniciar o redis:

```powershell
redis-server
```

### Alterar o settings.py

Altere o settings no:

```python
DATABASES = {
    'default': { 
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': 'gncdev', 
        'USER': 'postgres', 
        'PASSWORD': 'Arrebatamento2#', 
        'HOST': 'localhost', 
        'PORT': '3309', 
    }
}
```
para dadptar o db.

### Iniciar a VENV

A venv é quem esta com todas as bibliotecas salvas e é ela quem vai gerenciar a api.
Caso sua IDE nao inicie ela, digite no terminal:

```powershell
.venv/Scripts/activate
```

**Lembre-se: O terminal deve abrir a raiz do projeto**

### Subir as tabelas pro banco de dados

User o seguinte comando pra cirar as imigrações:

```powershell
python manage.py makemigrations
```

E para subi-las:

```powershell
python manage.py migrate
```

### Gere os testes

Para certifica-se que esta tudo bem gere os testes.

```shell
python manage.py test apps/gerenciaDev/tests
````

![Img test](https://github.com/josuelb/Gerenciador_Books/blob/9faf2ec526389418c0bf08b7ee7905d49f1df294/imgs_readme/tests_sucess.png)

### Iniciar a api
