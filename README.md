# SpassuBackEnd

## Descrição

Esta API REST desenvolvida em Django para uma plataforma de cursos gratuitos da Secretaria Municipal de Educação de São Paulo (SME-SP) em parceria com a Spassu Tecnologia. A plataforma permite a gestão de cursos, matrículas de usuários e integração com IA para geração automática de imagens de cursos.

## Funcionalidades

- **Gestão de Cursos**: Criar, listar, atualizar e deletar cursos
- **Autenticação JWT**: Sistema de login e registro de usuários
- **Matrículas**: Usuários podem se matricular em cursos
- **Geração de Imagens com IA**: Imagens de cursos geradas automaticamente usando OpenAI
- **Processamento Assíncrono**: Tarefas em background com Celery e Redis
- **API Documentada**: Endpoints documentados com Ninja API
- **Containerização**: Suporte a Docker e Docker Compose

## Tecnologias Utilizadas

- **Backend**: Django 6.0.1
- **API**: Django Ninja
- **Autenticação**: Django Ninja JWT
- **Banco de Dados**: SQLite (desenvolvimento)
- **Tarefas Assíncronas**: Celery + Redis
- **IA**: OpenAI API
- **Containerização**: Docker + Docker Compose
- **Testes**: Pytest + Coverage
- **Outros**: CORS headers, Pydantic, etc.

## Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- Conta OpenAI com API key

## Instalação e Configuração

### 1. Clonagem do Repositório

```bash
git clone <url-do-repositorio>
cd SpassuBackEnd
```

### 2. Ambiente Virtual (Opcional, se não usar Docker)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua-chave-openai-aqui
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_BROKER_URL_DOCKER=redis://redis:6379/0
```

### 4. Migrações do Banco

```bash
python manage.py migrate
```

## Executando o Projeto

### Com Docker (Recomendado)

```bash
docker-compose up --build
```

Isso iniciará:

- API Django na porta 8000
- Redis na porta 6379
- Worker Celery

### Sem Docker

```bash
# Terminal 1: Servidor Django
python manage.py runserver

# Terminal 2: Worker Celery
celery -A spassu worker -l info

# Terminal 3: Redis (se não estiver rodando)
redis-server
```

## Testes

```bash
pytest --cov=. --cov-report=html -v
```

Os relatórios de cobertura estarão em `htmlcov/index.html`.

## API Endpoints

### Cursos (Courses)

- `GET /api/courses/` - Lista todos os cursos publicados
- `GET /api/courses/{id}` - Detalhes de um curso
- `POST /api/courses/` - Criar curso (admin)
- `PUT /api/courses/{id}` - Atualizar curso (admin)
- `DELETE /api/courses/{id}` - Deletar curso (admin)
- `GET /api/courses/{id}/video` - Vídeo do curso (usuário matriculado)

### Autenticação (Auth)

- `POST /api/auth/register` - Registrar usuário
- `POST /api/auth/login` - Login (retorna tokens JWT)
- `POST /api/auth/refresh` - Refresh token

### Matrículas (Enrollments)

- `POST /api/enrollments/` - Matricular em curso
- `GET /api/enrollments/` - Listar matrículas do usuário

## Estrutura do Projeto

```
SpassuBackEnd/
├── courses/          # App de cursos
│   ├── models.py     # Modelos Course e Enrollment
│   ├── api.py        # Endpoints da API
│   ├── schemas.py    # Schemas Pydantic
│   ├── tasks.py      # Tarefas Celery
│   └── tests.py      # Testes
├── users/            # App de usuários
│   ├── api.py        # Endpoints de auth
│   └── schemas.py    # Schemas de usuário
├── services/         # Lógica de negócio
│   ├── course_service.py
│   └── openai_service.py
├── spassu/           # Configurações Django
├── media/            # Arquivos de mídia
├── assets/           # Arquivos estáticos
├── tests/            # Testes globais
├── docker-compose.yml
├── dockerfile
├── requirements.txt
└── pytest.ini
```

## Desenvolvimento

### Criando um Superusuário

```bash
python manage.py createsuperuser
```

### Admin Django

Acesse `http://localhost:8000/admin/` para interface administrativa.

## Deploy

Para produção, considere:

- Usar PostgreSQL ao invés de SQLite
- Configurar variáveis de produção
- Usar Gunicorn ou similar
- Configurar Nginx como proxy reverso
- Gerenciar secrets adequadamente

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

MIT

## Contato

Para dúvidas ou sugestões, entre em contato com a equipe de desenvolvimento.
