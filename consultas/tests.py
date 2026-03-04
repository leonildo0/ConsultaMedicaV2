from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils.timezone import now
from django.db import IntegrityError

from .models import Paciente, Medico, Consulta, Pagamento, Atendimento, Exame, AtendimentoExame


class SistemaTestCase(TestCase):
    """
    Suite de testes para o sistema Consultas Médicas V2.
    Cobre autenticação, CRUD de entidades principais e permissões.
    """

    def setUp(self):
        """Configuração inicial para todos os testes."""
        self.client = Client()

        # Criar grupos de permissão
        self.grupo_admin = Group.objects.create(name="admin")
        self.grupo_atendente = Group.objects.create(name="Atendente")

        # Usuário administrador
        self.user_admin = User.objects.create_user(
            username="admin",
            password="123456"
        )
        self.user_admin.groups.add(self.grupo_admin)

        # Usuário comum (sem permissões especiais)
        self.user_comum = User.objects.create_user(
            username="usuario",
            password="123456"
        )

        # Usuário atendente
        self.user_atendente = User.objects.create_user(
            username="atendente",
            password="123456"
        )
        self.user_atendente.groups.add(self.grupo_atendente)

        # Dados de teste
        self.paciente = Paciente.objects.create(
            nome="João Teste",
            telefone="999999999",
            cpf='12345678900'
        )

        self.medico = Medico.objects.create(
            nome="Dr. Silva",
            crm="12345",
            telefone="888888888",
            especialidade="Clínico Geral",
            dias_atendimento=["segunda", "quarta", "sexta"]
        )

        self.exame = Exame.objects.create(
            nome="Hemograma",
            valor=50.00
        )

    # =============================
    # 🔐 TESTES DE AUTENTICAÇÃO
    # =============================

    def test_login_valido(self):
        """CT01: Login com credenciais válidas deve permitir acesso."""
        response = self.client.login(username="admin", password="123456")
        self.assertTrue(response)

    def test_login_invalido(self):
        """CT02: Login com senha incorreta deve falhar."""
        response = self.client.login(username="admin", password="errado")
        self.assertFalse(response)

    def test_login_usuario_inexistente(self):
        """CT03: Login com usuário inexistente deve falhar."""
        response = self.client.login(username="naoexiste", password="123456")
        self.assertFalse(response)

    def test_logout(self):
        """CT04: Logout deve encerrar a sessão."""
        self.client.login(username="admin", password="123456")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        # Após logout, acessar página protegida deve redirecionar
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_acesso_sem_login_redireciona(self):
        """CT05: Acesso a página protegida sem login deve redirecionar."""
        response = self.client.get(reverse("pacientes_lista"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    # =============================
    # 👤 TESTES CRUD PACIENTE
    # =============================

    def test_criar_paciente(self):
        """CT07: Criar paciente com dados válidos."""
        novo = Paciente.objects.create(
            nome="Maria Teste",
            telefone="777777777",
            cpf='22222222200'
        )
        self.assertEqual(Paciente.objects.count(), 2)
        self.assertEqual(novo.nome, "Maria Teste")

    def test_editar_paciente(self):
        """CT09: Editar dados de um paciente existente."""
        self.paciente.nome = "João Atualizado"
        self.paciente.save()
        paciente = Paciente.objects.get(id=self.paciente.id)
        self.assertEqual(paciente.nome, "João Atualizado")

    def test_excluir_paciente(self):
        """Excluir paciente do banco de dados."""
        self.paciente.delete()
        self.assertEqual(Paciente.objects.count(), 0)

    def test_listar_pacientes_view(self):
        """CT06: Listar pacientes via view."""
        self.client.login(username="admin", password="123456")
        response = self.client.get(reverse("pacientes_lista"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "João Teste")

    def test_criar_paciente_cpf_duplicado(self):
        """CT08: Criar paciente com CPF duplicado deve falhar."""
        with self.assertRaises(IntegrityError):
            Paciente.objects.create(
                nome="Outro Paciente",
                telefone="666666666",
                cpf='12345678900'  # CPF já existe
            )

    def test_criar_paciente_via_view(self):
        """Criar paciente através do formulário."""
        self.client.login(username="admin", password="123456")
        response = self.client.post(reverse("pacientes_criar"), {
            'nome': 'Novo Paciente',
            'cpf': '99999999999',
            'telefone': '555555555'
        })
        self.assertEqual(response.status_code, 302)  # Redirect após sucesso
        self.assertTrue(Paciente.objects.filter(cpf='99999999999').exists())

    def test_admin_pode_excluir_paciente(self):
        """CT10: Admin pode excluir paciente."""
        self.client.login(username="admin", password="123456")
        response = self.client.post(reverse("pacientes_excluir", args=[self.paciente.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Paciente.objects.filter(id=self.paciente.id).exists())

    def test_usuario_comum_nao_pode_excluir_paciente(self):
        """CT11: Usuário sem permissão não pode excluir paciente."""
        self.client.login(username="usuario", password="123456")
        response = self.client.post(reverse("pacientes_excluir", args=[self.paciente.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Paciente.objects.filter(id=self.paciente.id).exists())

    # =============================
    # 📅 TESTES CRUD CONSULTA
    # =============================

    def test_criar_consulta(self):
        """CT19: Criar consulta com dados válidos."""
        consulta = Consulta.objects.create(
            paciente=self.paciente,
            medico=self.medico,
            data=now().date()
        )
        self.assertEqual(Consulta.objects.count(), 1)
        self.assertEqual(consulta.paciente.nome, "João Teste")

    def test_listar_consultas_view(self):
        """CT18: Listar consultas (agenda) via view."""
        Consulta.objects.create(
            paciente=self.paciente,
            medico=self.medico,
            data=now().date()
        )
        self.client.login(username="admin", password="123456")
        response = self.client.get(reverse("consultas_agenda"))
        self.assertEqual(response.status_code, 200)

    def test_admin_pode_excluir_consulta(self):
        """CT22: Admin pode excluir consulta."""
        consulta = Consulta.objects.create(
            paciente=self.paciente,
            medico=self.medico,
            data=now().date()
        )
        self.client.login(username="admin", password="123456")
        response = self.client.post(reverse("consultas_excluir", args=[consulta.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Consulta.objects.filter(id=consulta.id).exists())

    # =============================
    # 📊 TESTES DASHBOARD
    # =============================

    def test_dashboard_acesso_logado(self):
        """CT26: Dashboard acessível para usuário logado."""
        self.client.login(username="admin", password="123456")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_sem_login(self):
        """Dashboard sem login deve redirecionar."""
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_exibe_consultas_hoje(self):
        """CT27: Dashboard exibe consultas do dia."""
        Consulta.objects.create(
            paciente=self.paciente,
            medico=self.medico,
            data=now().date()
        )
        self.client.login(username="admin", password="123456")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertIn('consultas_hoje', response.context)
        self.assertEqual(response.context['total_consultas_hoje'], 1)

    # =============================
    # 🔒 TESTES DE PERMISSÃO
    # =============================

    def test_usuario_sem_permissao_dashboard(self):
        """Usuário comum pode acessar dashboard."""
        self.client.login(username="usuario", password="123456")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_atendente_acessa_pagamentos(self):
        """CT23: Atendente pode acessar pagamentos."""
        self.client.login(username="atendente", password="123456")
        response = self.client.get(reverse("pagamentos_lista"))
        self.assertEqual(response.status_code, 200)

    def test_usuario_comum_nao_acessa_pagamentos(self):
        """CT24: Usuário comum não pode acessar pagamentos."""
        self.client.login(username="usuario", password="123456")
        response = self.client.get(reverse("pagamentos_lista"))
        self.assertEqual(response.status_code, 403)

    # =============================
    # 👨‍⚕️ TESTES CRUD MÉDICO
    # =============================

    def test_criar_medico(self):
        """CT13: Criar médico com dados válidos."""
        medico = Medico.objects.create(
            nome="Dra. Ana",
            crm="54321",
            telefone="777777777",
            especialidade="Pediatra",
            dias_atendimento=["terca", "quinta"]
        )
        self.assertEqual(Medico.objects.count(), 2)
        self.assertEqual(medico.especialidade, "Pediatra")

    def test_listar_medicos_view(self):
        """CT12: Listar médicos via view."""
        self.client.login(username="admin", password="123456")
        response = self.client.get(reverse("medicos_lista"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dr. Silva")

    def test_criar_medico_crm_duplicado(self):
        """CT14: Criar médico com CRM duplicado deve falhar."""
        with self.assertRaises(IntegrityError):
            Medico.objects.create(
                nome="Dr. Outro",
                crm="12345",  # CRM já existe
                telefone="666666666",
                especialidade="Cardiologista",
                dias_atendimento=["segunda"]
            )

    def test_medico_dias_atendimento(self):
        """CT16: Verificar dias de atendimento do médico."""
        self.assertIn("segunda", self.medico.dias_atendimento)
        self.assertIn("quarta", self.medico.dias_atendimento)
        self.assertNotIn("domingo", self.medico.dias_atendimento)

    def test_admin_pode_excluir_medico(self):
        """CT17: Admin pode excluir médico."""
        self.client.login(username="admin", password="123456")
        response = self.client.post(reverse("medicos_excluir", args=[self.medico.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Medico.objects.filter(id=self.medico.id).exists())

    # =============================
    # 🔄 TESTES AJAX
    # =============================

    def test_ajax_carregar_medicos(self):
        """CT20: AJAX retorna médicos disponíveis para a data."""
        self.client.login(username="admin", password="123456")
        # Segunda-feira: 2026-03-02 é uma segunda
        response = self.client.get(reverse("carregar_medicos"), {'data': '2026-03-02'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('medicos', data)
        # Dr. Silva atende segunda, deve aparecer
        medico_ids = [m['id'] for m in data['medicos']]
        self.assertIn(self.medico.id, medico_ids)

    def test_ajax_carregar_medicos_dia_sem_atendimento(self):
        """AJAX não retorna médicos para dia sem atendimento."""
        self.client.login(username="admin", password="123456")
        # 2026-03-03 é terça, Dr. Silva não atende
        response = self.client.get(reverse("carregar_medicos"), {'data': '2026-03-03'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        medico_ids = [m['id'] for m in data['medicos']]
        self.assertNotIn(self.medico.id, medico_ids)
