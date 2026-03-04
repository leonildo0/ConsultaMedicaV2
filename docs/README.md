# Consultas Médicas V2

Sistema de gerenciamento de consultas médicas desenvolvido em Django 6.0.

## Stack Tecnológico

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Python | 3.12+ | Linguagem de programação |
| Django | 6.0 | Framework web |
| SQLite | 3 | Banco de dados (desenvolvimento) |
| HTML/CSS | 5/3 | Frontend com templates Django |

## Como Executar

### Pré-requisitos

- Python 3.12 ou superior instalado
- pip (gerenciador de pacotes Python)

### Instalação

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd ConsultaMedicaV2

# 2. Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar migrações do banco de dados
python manage.py migrate

# 5. Criar superusuário (opcional)
python manage.py createsuperuser

# 6. Iniciar servidor de desenvolvimento
python manage.py runserver
```

O sistema estará disponível em `http://127.0.0.1:8000/`

### Comandos Úteis

```bash
# Executar todos os testes
python manage.py test

# Executar teste específico
python manage.py test consultas.tests.SistemaTestCase.test_criar_consulta

# Criar novas migrações após alterar models
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate
```

## Estrutura do Projeto

```
ConsultaMedicaV2/
├── consultas/                 # App principal
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Views/Controllers
│   ├── urls.py                # Rotas da aplicação
│   ├── forms.py               # Formulários
│   ├── decorators.py          # Decorators customizados
│   ├── tests.py               # Testes unitários
│   └── migrations/            # Migrações do banco
├── consultas_medicasV2/       # Configurações Django
│   ├── settings.py            # Configurações gerais
│   ├── urls.py                # Rotas principais
│   └── wsgi.py                # WSGI para deploy
├── templates/                 # Templates HTML
│   ├── base.html              # Template base
│   ├── dashboard.html         # Dashboard principal
│   ├── pacientes/             # Templates de pacientes
│   ├── medicos/               # Templates de médicos
│   ├── consultas/             # Templates de consultas
│   ├── pagamentos/            # Templates de pagamentos
│   ├── exames/                # Templates de exames
│   └── registration/          # Templates de autenticação
├── docs/                      # Documentação do projeto
├── manage.py                  # CLI do Django
├── requirements.txt           # Dependências
└── db.sqlite3                 # Banco de dados SQLite
```

## Arquitetura do Sistema

### Diagrama de Modelos

```
┌─────────────┐       ┌─────────────┐
│  Paciente   │       │   Medico    │
├─────────────┤       ├─────────────┤
│ nome        │       │ nome        │
│ cpf (único) │       │ crm (único) │
│ telefone    │       │ telefone    │
│             │       │ especialidade│
│             │       │ dias_atendimento (JSON)
└──────┬──────┘       └──────┬──────┘
       │                     │
       │    ┌────────────────┤
       │    │                │
       ▼    ▼                │
┌─────────────────┐          │
│    Consulta     │◄─────────┘
├─────────────────┤
│ data            │
│ paciente (FK)   │
│ medico (FK)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌─────────────┐
│Pagamento│ │ Atendimento │
├─────────┤ ├─────────────┤
│valor    │ │descricao    │
│data_pag │ │data_atend   │
│forma_pag│ │exames (M2M) │
│pago     │ └──────┬──────┘
└─────────┘        │
                   │ through
                   ▼
           ┌──────────────────┐
           │ AtendimentoExame │
           ├──────────────────┤
           │ atendimento (FK) │
           │ exame (FK)       │
           │ status           │
           │ (solicitado/     │
           │  realizado/      │
           │  entregue)       │
           └──────────────────┘
                   │
                   ▼
             ┌──────────┐
             │  Exame   │
             ├──────────┤
             │ nome     │
             │ valor    │
             └──────────┘
```

### Relacionamentos

| Modelo | Relacionamento | Descrição |
|--------|---------------|-----------|
| Consulta | ForeignKey → Paciente | Cada consulta pertence a um paciente |
| Consulta | ForeignKey → Medico | Cada consulta é realizada por um médico |
| Pagamento | OneToOne → Consulta | Cada consulta tem um pagamento |
| Atendimento | OneToOne → Consulta | Cada consulta tem um atendimento |
| AtendimentoExame | ForeignKey → Atendimento | Tabela intermediária para exames |
| AtendimentoExame | ForeignKey → Exame | Exames solicitados no atendimento |

## Funcionalidades

### Autenticação e Segurança

- **Login/Logout**: Sistema de autenticação Django
- **Controle de Acesso**: Decorator `@login_required` para views protegidas
- **Permissões por Grupo**: Decorator customizado `@grupo_required("nome_grupo")`

### Grupos de Usuários

| Grupo | Permissões |
|-------|------------|
| admin | Pode excluir qualquer registro |
| Atendente | Acesso ao módulo de pagamentos |

### CRUD de Entidades

Todas as entidades seguem o padrão:

| Operação | URL | View |
|----------|-----|------|
| Listar | `/{entidade}/` | `{entidade}_lista` |
| Criar | `/{entidade}/novo/` | `{entidade}_criar` |
| Editar | `/{entidade}/<id>/editar/` | `{entidade}_editar` |
| Excluir | `/{entidade}/<id>/excluir/` | `{entidade}_excluir` |

### Dashboard

- Consultas do dia
- Exames pendentes
- Estatísticas (total de pacientes, médicos, consultas)
- Gráficos de consultas e exames por mês

### Disponibilidade de Médicos

O campo `dias_atendimento` armazena os dias da semana (em português sem acento):
- `['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']`

Ao criar uma consulta, o sistema filtra médicos disponíveis via AJAX (`/ajax/carregar-medicos/`).

## Padrões de Código

### Formulários

Todos os formulários usam o padrão:

```python
form = ModelForm(request.POST or None, instance=obj)
if form.is_valid():
    form.save()
    return redirect('lista')
```

### Templates

- `base.html`: Template base com navbar e sidebar
- Cada entidade herda de `base.html`
- Estrutura: `lista.html`, `form.html`, `excluir.html`

### Idioma

O código utiliza português brasileiro para:
- Nomes de modelos (Paciente, Medico, Consulta)
- Campos (nome, cpf, telefone, data_pagamento)
- URLs e views (pacientes_lista, medicos_criar)

## Credenciais de Teste

Consulte o arquivo `superusuario.txt` para credenciais do superusuário de desenvolvimento.
