# Plano de Manutenção - Consultas Médicas V2

## 1. Introdução

Este documento descreve o plano de manutenção para o sistema Consultas Médicas V2, incluindo estratégias para manutenção corretiva, adaptativa e evolutiva.

## 2. Tipos de Manutenção

### 2.1 Manutenção Corretiva

Correção de defeitos identificados durante os testes ou uso do sistema.

| ID | Descrição do Problema | Módulo Afetado | Prioridade | Status |
|----|----------------------|----------------|------------|--------|
| MC01 | Grupo "admin" não criado automaticamente | Autenticação | Alta | Pendente |
| MC02 | Validação de CPF não verifica formato | Pacientes | Média | Pendente |
| MC03 | Validação de CRM não verifica formato | Médicos | Média | Pendente |
| MC04 | Domingo não está no mapa de dias | Consultas | Baixa | Identificado |

### 2.2 Manutenção Adaptativa

Adequação do sistema a novos ambientes ou requisitos externos.

| ID | Descrição | Justificativa | Prioridade | Status |
|----|-----------|---------------|------------|--------|
| MA01 | Migração para PostgreSQL | Produção requer banco robusto | Alta | Planejado |
| MA02 | Atualização Django 6.x → 7.x | Suporte a longo prazo | Média | Futuro |
| MA03 | Containerização com Docker | Padronização de ambiente | Média | Planejado |
| MA04 | Deploy em nuvem (Heroku/AWS) | Acesso remoto ao sistema | Alta | Planejado |

### 2.3 Manutenção Evolutiva

Inclusão de novas funcionalidades para melhorar o sistema.

| ID | Descrição | Benefício | Prioridade | Status |
|----|-----------|-----------|------------|--------|
| ME01 | Recuperação de senha por email | Segurança e usabilidade | Alta | Planejado |
| ME02 | Exportação de relatórios em PDF | Documentação de consultas | Média | Planejado |
| ME03 | API REST para integração | Interoperabilidade | Média | Futuro |
| ME04 | Notificações por email/SMS | Lembrete de consultas | Baixa | Futuro |
| ME05 | Histórico de alterações (audit log) | Rastreabilidade | Média | Planejado |
| ME06 | Busca e filtros avançados | Usabilidade | Média | Planejado |

## 3. Procedimentos de Manutenção

### 3.1 Processo de Correção de Bugs

```
1. Identificação do problema
   ↓
2. Registro no Relatório de Incidentes
   ↓
3. Análise de impacto
   ↓
4. Desenvolvimento da correção
   ↓
5. Criação de teste para o bug
   ↓
6. Revisão de código
   ↓
7. Deploy em ambiente de teste
   ↓
8. Validação
   ↓
9. Deploy em produção
```

### 3.2 Processo de Atualização

```
1. Backup do banco de dados
   ↓
2. Backup do código fonte
   ↓
3. Atualização em ambiente de desenvolvimento
   ↓
4. Execução de testes
   ↓
5. Validação de compatibilidade
   ↓
6. Deploy em ambiente de homologação
   ↓
7. Testes de regressão
   ↓
8. Deploy em produção
```

### 3.3 Processo de Nova Funcionalidade

```
1. Levantamento de requisitos
   ↓
2. Análise de viabilidade
   ↓
3. Design da solução
   ↓
4. Implementação
   ↓
5. Criação de testes
   ↓
6. Documentação
   ↓
7. Revisão de código
   ↓
8. Deploy
```

## 4. Cronograma de Manutenção

| Período | Atividade | Tipo |
|---------|-----------|------|
| Semana 1 | Correção de bugs identificados nos testes | Corretiva |
| Semana 2 | Implementação de recuperação de senha | Evolutiva |
| Semana 3 | Configuração de Docker | Adaptativa |
| Semana 4 | Exportação de relatórios PDF | Evolutiva |

## 5. Métricas de Manutenção

| Métrica | Meta |
|---------|------|
| Tempo médio de correção (bugs críticos) | < 24 horas |
| Tempo médio de correção (bugs médios) | < 1 semana |
| Cobertura de testes após manutenção | ≥ 70% |
| Testes de regressão passando | 100% |

## 6. Responsabilidades

| Papel | Responsabilidades |
|-------|-------------------|
| Desenvolvedor | Implementar correções e novas funcionalidades |
| Testador | Validar correções e executar testes de regressão |
| DBA | Gerenciar backups e migrações de banco |
| DevOps | Gerenciar deploys e infraestrutura |

## 7. Documentação de Suporte

| Documento | Descrição |
|-----------|-----------|
| `docs/README.md` | Documentação técnica do sistema |
| `docs/PLANO_DE_TESTE.md` | Plano de testes |
| `docs/CASOS_DE_TESTE.md` | Casos de teste detalhados |
| `docs/RELATORIO_DE_TESTE.md` | Resultados dos testes |
| `.github/copilot-instructions.md` | Instruções para desenvolvimento |

## 8. Controle de Versão

| Versão | Data | Alterações |
|--------|------|------------|
| 1.0.0 | - | Versão inicial do sistema |
| 1.0.1 | - | Correções de bugs dos testes |
| 1.1.0 | - | Recuperação de senha (planejado) |
| 1.2.0 | - | Exportação PDF (planejado) |

## 9. Backup e Recuperação

### 9.1 Política de Backup

| Tipo | Frequência | Retenção |
|------|------------|----------|
| Banco de dados completo | Diário | 30 dias |
| Código fonte | A cada commit | Indefinido (Git) |
| Arquivos de configuração | Semanal | 90 dias |

### 9.2 Procedimento de Recuperação

```bash
# Restaurar banco de dados SQLite
cp backup/db.sqlite3 ./db.sqlite3

# Restaurar código fonte
git checkout <commit-hash>

# Recriar migrações se necessário
python manage.py migrate
```

## 10. Contatos

| Função | Contato |
|--------|---------|
| Suporte Técnico | [email do desenvolvedor] |
| Emergências | [telefone] |
