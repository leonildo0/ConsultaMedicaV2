# Copilot Instructions - Consultas Médicas V2

Sistema de gerenciamento de consultas médicas desenvolvido em Django 6.0.

## Comandos

```bash
# Executar servidor de desenvolvimento
python manage.py runserver

# Executar todas as migrações
python manage.py migrate

# Criar novas migrações após alterar models
python manage.py makemigrations

# Executar todos os testes
python manage.py test

# Executar um teste específico
python manage.py test consultas.tests.SistemaTestCase.test_criar_consulta
```

## Arquitetura

### Estrutura do Projeto

- `consultas/` - App principal com toda a lógica de negócio
- `consultas_medicasV2/` - Configurações do projeto Django
- `templates/` - Templates HTML organizados por entidade (pacientes/, medicos/, consultas/, etc.)

### Modelos e Relacionamentos

O sistema possui uma hierarquia de relacionamentos centrada em `Consulta`:

```
Paciente ─┬─► Consulta ◄─┬─ Medico
          │              │
          │      ┌───────┴───────┐
          │      ▼               ▼
          │  Pagamento      Atendimento
          │  (1:1)              │
          │                     ▼
          │              AtendimentoExame ◄── Exame
          │                (through)
```

- `Consulta` conecta `Paciente` e `Medico` com uma data
- `Pagamento` é 1:1 com `Consulta`
- `Atendimento` é 1:1 com `Consulta` e contém exames solicitados
- `AtendimentoExame` é a tabela intermediária com status (solicitado/realizado/entregue)

### Padrão de Views CRUD

Todas as entidades seguem o mesmo padrão de nomenclatura:

```python
# Lista
{entidade}_lista(request)

# Criar
{entidade}_criar(request)

# Editar
{entidade}_editar(request, id)

# Excluir
{entidade}_excluir(request, id)
```

URLs correspondentes: `{entidade}/`, `{entidade}/novo/`, `{entidade}/<id>/editar/`, `{entidade}/<id>/excluir/`

## Convenções

### Controle de Acesso

- `@login_required` - Requer autenticação
- `@grupo_required("nome_grupo")` - Decorator customizado em `consultas/decorators.py` que verifica se o usuário pertence ao grupo especificado

Grupos utilizados:
- `admin` - Pode excluir qualquer registro
- `Atendente` - Acesso a pagamentos

### Disponibilidade de Médicos

O campo `dias_atendimento` em `Medico` é um `JSONField` contendo lista de dias da semana em português sem acento:
`['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']`

Ao criar consultas, o formulário filtra médicos disponíveis via AJAX em `/ajax/carregar-medicos/`.

### Padrão de Formulários

Todos os forms usam o padrão `request.POST or None` para lidar com GET/POST:

```python
form = ModelForm(request.POST or None, instance=obj)
if form.is_valid():
    form.save()
    return redirect('lista')
```

### Templates

- `base.html` contém navbar e sidebar com menu de navegação
- Templates de cada entidade herdam de `base.html`
- Cada entidade tem: `lista.html`, `form.html`, `excluir.html`

### Idioma

O código usa português brasileiro para nomes de modelos, campos e variáveis (paciente, medico, consulta, pagamento, etc.).
