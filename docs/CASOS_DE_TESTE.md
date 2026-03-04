# Casos de Teste - Consultas Médicas V2

## Legenda

- **ID**: Identificador único do caso de teste
- **Pré-condições**: Estado necessário antes da execução
- **Passos**: Ações a serem executadas
- **Resultado Esperado**: Comportamento correto do sistema

---

## 1. Testes de Autenticação

| ID | Descrição | Pré-condições | Passos | Resultado Esperado |
|----|-----------|---------------|--------|-------------------|
| CT01 | Login com credenciais válidas | Usuário cadastrado no sistema | 1. Acessar `/accounts/login/` 2. Inserir usuário e senha válidos 3. Clicar em "Entrar" | Sistema permite acesso e redireciona para Dashboard |
| CT02 | Login com senha incorreta | Usuário cadastrado no sistema | 1. Acessar `/accounts/login/` 2. Inserir usuário válido e senha incorreta 3. Clicar em "Entrar" | Sistema exibe mensagem de erro e permanece na tela de login |
| CT03 | Login com usuário inexistente | Nenhum usuário com esse nome | 1. Acessar `/accounts/login/` 2. Inserir usuário inexistente 3. Clicar em "Entrar" | Sistema exibe mensagem de erro |
| CT04 | Logout do sistema | Usuário autenticado | 1. Clicar em "Sair" na navbar | Sessão encerrada, redirecionamento para login |
| CT05 | Acesso a página protegida sem login | Usuário não autenticado | 1. Acessar `/pacientes/` diretamente | Redirecionamento para `/accounts/login/` |

---

## 2. Testes CRUD - Pacientes

| ID | Descrição | Pré-condições | Passos | Resultado Esperado |
|----|-----------|---------------|--------|-------------------|
| CT06 | Listar pacientes | Usuário autenticado, pacientes cadastrados | 1. Acessar `/pacientes/` | Lista de pacientes exibida |
| CT07 | Criar paciente com dados válidos | Usuário autenticado | 1. Acessar `/pacientes/novo/` 2. Preencher nome, CPF e telefone 3. Submeter formulário | Paciente criado, redirecionamento para lista |
| CT08 | Criar paciente com CPF duplicado | Paciente com mesmo CPF já existe | 1. Acessar `/pacientes/novo/` 2. Preencher dados com CPF existente 3. Submeter formulário | Erro de validação exibido |
| CT09 | Editar paciente | Usuário autenticado, paciente existente | 1. Acessar `/pacientes/<id>/editar/` 2. Alterar nome 3. Submeter formulário | Dados atualizados no banco |
| CT10 | Excluir paciente (admin) | Usuário do grupo "admin" | 1. Acessar `/pacientes/<id>/excluir/` 2. Confirmar exclusão | Paciente removido do banco |
| CT11 | Excluir paciente (sem permissão) | Usuário comum (não admin) | 1. Acessar `/pacientes/<id>/excluir/` | Erro 403 - Permissão negada |

---

## 3. Testes CRUD - Médicos

| ID | Descrição | Pré-condições | Passos | Resultado Esperado |
|----|-----------|---------------|--------|-------------------|
| CT12 | Listar médicos | Usuário autenticado | 1. Acessar `/medicos/` | Lista de médicos exibida |
| CT13 | Criar médico com dados válidos | Usuário autenticado | 1. Acessar `/medicos/novo/` 2. Preencher nome, CRM, telefone, especialidade, dias 3. Submeter | Médico criado |
| CT14 | Criar médico com CRM duplicado | Médico com mesmo CRM já existe | 1. Acessar `/medicos/novo/` 2. Preencher dados com CRM existente 3. Submeter | Erro de validação |
| CT15 | Editar médico | Usuário autenticado, médico existente | 1. Acessar `/medicos/<id>/editar/` 2. Alterar especialidade 3. Submeter | Dados atualizados |
| CT16 | Verificar dias de atendimento | Médico com dias configurados | 1. Acessar detalhes do médico | Dias de atendimento exibidos corretamente |
| CT17 | Excluir médico (admin) | Usuário do grupo "admin" | 1. Acessar `/medicos/<id>/excluir/` 2. Confirmar | Médico removido |

---

## 4. Testes CRUD - Consultas

| ID | Descrição | Pré-condições | Passos | Resultado Esperado |
|----|-----------|---------------|--------|-------------------|
| CT18 | Listar consultas (agenda) | Usuário autenticado | 1. Acessar `/consultas/` | Agenda de consultas exibida |
| CT19 | Criar consulta | Paciente e médico cadastrados | 1. Acessar `/consultas/nova/` 2. Selecionar data 3. Selecionar paciente e médico 4. Submeter | Consulta criada |
| CT20 | Filtrar médicos por data (AJAX) | Médico com dias configurados | 1. Acessar `/consultas/nova/` 2. Selecionar uma segunda-feira | Apenas médicos que atendem segunda são exibidos |
| CT21 | Editar consulta | Consulta existente | 1. Acessar `/consultas/<id>/editar/` 2. Alterar data 3. Submeter | Consulta atualizada |
| CT22 | Excluir consulta (admin) | Usuário admin | 1. Acessar `/consultas/<id>/excluir/` 2. Confirmar | Consulta removida |

---

## 5. Testes de Permissões

| ID | Descrição | Pré-condições | Passos | Resultado Esperado |
|----|-----------|---------------|--------|-------------------|
| CT23 | Acesso a pagamentos (Atendente) | Usuário do grupo "Atendente" | 1. Acessar `/pagamentos/` | Lista de pagamentos exibida |
| CT24 | Acesso a pagamentos (sem permissão) | Usuário comum | 1. Acessar `/pagamentos/` | Erro 403 - Permissão negada |
| CT25 | Admin pode excluir qualquer registro | Usuário do grupo "admin" | 1. Excluir paciente, médico ou consulta | Exclusão permitida |

---

## 6. Testes do Dashboard

| ID | Descrição | Pré-condições | Passos | Resultado Esperado |
|----|-----------|---------------|--------|-------------------|
| CT26 | Acesso ao dashboard | Usuário autenticado | 1. Acessar `/` | Dashboard exibido com estatísticas |
| CT27 | Exibição de consultas do dia | Consultas agendadas para hoje | 1. Acessar `/` | Consultas do dia listadas |
| CT28 | Exibição de exames pendentes | Exames com status "solicitado" | 1. Acessar `/` | Exames pendentes listados |
| CT29 | Gráficos de consultas por mês | Consultas cadastradas | 1. Acessar `/` | Gráfico de consultas renderizado |

---

## Mapeamento: Casos de Teste → Testes Unitários

| Caso de Teste | Método de Teste |
|---------------|-----------------|
| CT01 | `test_login_valido` |
| CT02 | `test_login_invalido` |
| CT03 | `test_login_usuario_inexistente` |
| CT04 | `test_logout` |
| CT05 | `test_acesso_sem_login_redireciona` |
| CT06 | `test_listar_pacientes_view` |
| CT07 | `test_criar_paciente` |
| CT08 | `test_criar_paciente_cpf_duplicado` |
| CT09 | `test_editar_paciente` |
| CT10 | `test_admin_pode_excluir_paciente` |
| CT11 | `test_usuario_comum_nao_pode_excluir_paciente` |
| CT12 | `test_listar_medicos_view` |
| CT13 | `test_criar_medico` |
| CT14 | `test_criar_medico_crm_duplicado` |
| CT15 | `test_editar_medico` |
| CT16 | `test_medico_dias_atendimento` |
| CT17 | `test_admin_pode_excluir_medico` |
| CT18 | `test_listar_consultas_view` |
| CT19 | `test_criar_consulta` |
| CT20 | `test_ajax_carregar_medicos` |
| CT21 | `test_editar_consulta` |
| CT22 | `test_admin_pode_excluir_consulta` |
| CT26 | `test_dashboard_acesso_logado` |
| CT27 | `test_dashboard_exibe_consultas_hoje` |
