from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils.timezone import now

from .models import Paciente, Medico, Consulta, Pagamento, Atendimento, Exame, AtendimentoExame


from consultas.models import Consulta



class SistemaTestCase(TestCase):

    def setUp(self):
        # Cliente para simular requisições
        self.client = Client()

        # Criar grupos
        self.grupo_admin = Group.objects.create(name="Administrador")
        self.grupo_medico = Group.objects.create(name="Medico")

        # Criar usuário admin
        self.user_admin = User.objects.create_user(
            username="admin",
            password="123456"
        )
        self.user_admin.groups.add(self.grupo_admin)

        # Criar paciente
        self.paciente = Paciente.objects.create(
            nome="João Teste",
            telefone="999999999",
            cpf ='12345678900'
        )

        # Criar médico
        self.medico = Medico.objects.create(
            nome="Dr. Silva",
            crm="12345",
            telefone="888888888",
            especialidade="Clínico Geral",
            dias_atendimento=["segunda"]
        )

    # =============================
    # 🔐 TESTE DE LOGIN
    # =============================

    def test_login_valido(self):
        response = self.client.login(username="admin", password="123456")
        self.assertTrue(response)

    def test_login_invalido(self):
        response = self.client.login(username="admin", password="errado")
        self.assertFalse(response)

    # =============================
    # 👤 TESTE CRUD PACIENTE
    # =============================

    def test_criar_paciente(self):
        novo = Paciente.objects.create(
            nome="Maria Teste",
            telefone="777777777",
            cpf = '22222222200'
        )
        self.assertEqual(Paciente.objects.count(), 2)
        self.assertEqual(novo.nome, "Maria Teste")

    def test_editar_paciente(self):
        self.paciente.nome = "João Atualizado"
        self.paciente.save()
        paciente = Paciente.objects.get(id=self.paciente.id)
        self.assertEqual(paciente.nome, "João Atualizado")

    def test_excluir_paciente(self):
        self.paciente.delete()
        self.assertEqual(Paciente.objects.count(), 0)

    # =============================
    # 📅 TESTE CRIAÇÃO DE CONSULTA
    # =============================

    def test_criar_consulta(self):
        consulta = Consulta.objects.create(
            paciente=self.paciente,
            medico=self.medico,
            data=now().date()
        )
        self.assertEqual(Consulta.objects.count(), 1)
        self.assertEqual(consulta.paciente.nome, "João Teste")

    # =============================
    # 📊 TESTE DASHBOARD
    # =============================

    def test_dashboard_acesso_logado(self):
        self.client.login(username="admin", password="123456")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_sem_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)  # redireciona

    # =============================
    # 🔒 TESTE PERMISSÃO
    # =============================

    def test_usuario_sem_permissao(self):
        user = User.objects.create_user(
            username="usuario",
            password="123456"
        )

        self.client.login(username="usuario", password="123456")
        response = self.client.get(reverse("dashboard"))
        
        
        self.assertIn(response.status_code, [200])

# Create your tests here.
