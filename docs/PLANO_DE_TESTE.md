# Plano de Teste - Consultas Médicas V2

## 1. Introdução

Este documento descreve o plano de testes para o sistema Consultas Médicas V2, um sistema de gerenciamento de consultas médicas desenvolvido em Django 6.0.

## 2. Objetivos

- Garantir que todas as funcionalidades do sistema funcionem conforme especificado
- Identificar e documentar defeitos antes da entrega
- Validar a segurança do sistema (autenticação e autorização)
- Assegurar a integridade dos dados no banco de dados
- Verificar a usabilidade da interface do usuário

## 3. Escopo

### 3.1 Funcionalidades a Testar

| Módulo | Funcionalidades |
|--------|-----------------|
| Autenticação | Login, Logout, Controle de sessão |
| Pacientes | CRUD completo, Validações, Histórico |
| Médicos | CRUD completo, Dias de atendimento |
| Consultas | CRUD completo, Filtro de médicos por disponibilidade |
| Pagamentos | CRUD completo, Controle de permissões |
| Exames | CRUD completo, Status de exames |
| Atendimentos | Registro de atendimento, Solicitação de exames |
| Dashboard | Exibição de estatísticas, Gráficos |

### 3.2 Funcionalidades Fora do Escopo

- Recuperação de senha (não implementado)
- Integração com sistemas externos
- Testes de carga/stress

## 4. Tipos de Testes

### 4.1 Testes Unitários

Testes automatizados para validar:
- Criação, leitura, atualização e exclusão de modelos
- Validações de formulários
- Comportamento de views
- Decorators de permissão

**Ferramenta:** Django TestCase

### 4.2 Testes de Integração

Validação da comunicação entre:
- Views e Models
- Templates e Context
- Sistema de autenticação e controle de acesso

**Ferramenta:** Django Client

### 4.3 Testes Funcionais

Verificação de que o sistema atende aos requisitos:
- Fluxo completo de agendamento de consulta
- Fluxo de pagamento
- Fluxo de atendimento e solicitação de exames

**Método:** Testes manuais com checklist

### 4.4 Testes de Segurança

- Proteção de rotas autenticadas
- Controle de permissões por grupo
- Prevenção de acesso não autorizado

**Ferramenta:** Django TestCase com verificação de status codes

## 5. Ambiente de Teste

| Componente | Especificação |
|------------|---------------|
| Sistema Operacional | Linux / Windows |
| Python | 3.12+ |
| Django | 6.0 |
| Banco de Dados | SQLite (testes usam banco em memória) |
| Navegador | Chrome/Firefox (testes manuais) |

## 6. Critérios de Entrada

- Código fonte completo e funcional
- Ambiente de desenvolvimento configurado
- Banco de dados migrado
- Dependências instaladas

## 7. Critérios de Saída

- Todos os testes unitários passando (100%)
- Nenhum defeito crítico ou bloqueador em aberto
- Documentação de testes atualizada
- Relatório de testes preenchido

## 8. Cronograma

| Fase | Atividade | Status |
|------|-----------|--------|
| 1 | Análise do sistema e planejamento | ✅ Concluído |
| 2 | Definição dos casos de teste | ✅ Concluído |
| 3 | Implementação dos testes unitários | 🔄 Em andamento |
| 4 | Execução dos testes | ⏳ Pendente |
| 5 | Documentação dos resultados | ⏳ Pendente |

## 9. Responsáveis

| Papel | Responsável |
|-------|-------------|
| Desenvolvedor | Aluno |
| Testador | Aluno |
| Revisor | Colega de turma (troca de projetos) |

## 10. Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Ambiente não configurado | Baixa | Alto | Documentação de setup |
| Testes instáveis | Média | Médio | Uso de fixtures e setUp() |
| Falta de tempo | Média | Alto | Priorização de testes críticos |

## 11. Ferramentas

| Ferramenta | Uso |
|------------|-----|
| `python manage.py test` | Execução de testes unitários |
| Django Client | Simulação de requisições HTTP |
| Django TestCase | Framework de testes |
| SQLite in-memory | Banco de dados para testes |

## 12. Métricas

- **Cobertura de código**: Mínimo 70% das views principais
- **Taxa de sucesso**: 100% dos testes passando
- **Tempo de execução**: < 30 segundos para suite completa
