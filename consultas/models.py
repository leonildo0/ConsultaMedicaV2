from django.db import models


class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=100)
    crm = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=15)
    especialidade = models.CharField(max_length=100)

    DIAS_SEMANA = [
        ('segunda', 'Segunda'),
        ('terca', 'Terça'),
        ('quarta', 'Quarta'),
        ('quinta', 'Quinta'),
        ('sexta', 'Sexta'),
        ('sabado', 'Sábado'),
    ]

    dias_atendimento = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"


class Consulta(models.Model):
    data = models.DateField()
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        related_name='consultas'
    )
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='consultas'
    )

    def __str__(self):
        return f"{self.data} - {self.paciente} com {self.medico}"

class Pagamento(models.Model):
    consulta = models.OneToOneField(
        Consulta,
        on_delete=models.CASCADE,
        related_name='pagamento'
    )
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_pagamento = models.DateField()
    forma_pagamento = models.CharField(
        max_length=20,
        choices=[
            ('dinheiro', 'Dinheiro'),
            ('cartao', 'Cartão'),
            ('pix', 'PIX'),
        ]
    )
    pago = models.BooleanField(default=False)

    def __str__(self):
        status = "Pago" if self.pago else "Pendente"
        return f"{self.consulta} - {status}"
    
class Exame(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome
    
class AtendimentoExame(models.Model):
    STATUS_CHOICES = [
        ('solicitado', 'Solicitado'),
        ('realizado', 'Realizado'),
        ('entregue', 'Entregue'),
    ]

    atendimento = models.ForeignKey(
        'Atendimento',
        on_delete=models.CASCADE,
        related_name='exames_solicitados'
    )
    exame = models.ForeignKey(
        'Exame',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='solicitado'
    )

    def __str__(self):
        return f"{self.exame} - {self.get_status_display()}"

    
class Atendimento(models.Model):
    consulta = models.OneToOneField(
        Consulta,
        on_delete=models.CASCADE,
        related_name='atendimento'
    )
    descricao = models.TextField()
    exames = models.ManyToManyField(
        Exame,
        through='AtendimentoExame',
        blank=True
    )
    data_atendimento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Atendimento - {self.consulta}"
