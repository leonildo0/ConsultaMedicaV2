import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.db import models
from django.http import JsonResponse
from django.db.models.functions import TruncMonth


from .decorators import grupo_required

from datetime import datetime

from .forms import PacienteForm,MedicoForm, ConsultaForm, PagamentoForm, AtendimentoForm, ExameForm

from .models import Paciente, Medico, Consulta, Pagamento, Atendimento, Exame, AtendimentoExame


@login_required
def dashboard(request):
    hoje = now().date()

    consultas_hoje = Consulta.objects.select_related(
        'paciente', 'medico'
    ).filter(data=hoje)

    exames_pendentes = AtendimentoExame.objects.select_related(
        'atendimento__consulta__paciente',
        'exame'
    ).filter(status='solicitado')

    total_pacientes = Paciente.objects.count()
    total_medicos = Medico.objects.count()
    total_consultas_hoje = consultas_hoje.count()


    consultas_mes = (
        Consulta.objects
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total=models.Count('id'))
        .order_by('mes')
    )

    labels_consultas = [
        item['mes'].strftime('%B/%Y').capitalize()
        for item in consultas_mes
        if item['mes'] is not None
    ]

    dados_consultas = [
        item['total'] for item in consultas_mes
        if item['mes'] is not None
    ]

    exames_mes = (
    AtendimentoExame.objects
    .annotate(mes=TruncMonth('atendimento__consulta__data'))
    .values('mes')
    .annotate(total=models.Count('id'))
    .order_by('mes')
    )

    labels_exames = [
        item['mes'].strftime('%B/%Y').capitalize()
        for item in exames_mes
        if item['mes'] is not None
    ]

    dados_exames = [
        item['total']
        for item in exames_mes
        if item['mes'] is not None
   ]
    context = {
        'consultas_hoje': consultas_hoje,
        'total_pacientes': total_pacientes,
        'total_medicos': total_medicos,
        'total_consultas_hoje': total_consultas_hoje,
        'exames_pendentes': exames_pendentes,
        'total_exames_pendentes': exames_pendentes.count(),

        'labels_consultas': json.dumps(labels_consultas),
        'dados_consultas': json.dumps(dados_consultas),
        'labels_exames': json.dumps(labels_exames),
        'dados_exames': json.dumps(dados_exames),
    }

    

    return render(request, 'dashboard.html', context)




##### PACIENTES ####
@login_required
def pacientes_lista(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes})
@login_required
def pacientes_criar(request):
    form = PacienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('pacientes_lista')

    return render(request, 'pacientes/form.html', {'form': form})


@login_required
def pacientes_editar(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    form = PacienteForm(request.POST or None, instance=paciente)

    if form.is_valid():
        form.save()
        return redirect('pacientes_lista')

    return render(request, 'pacientes/form.html', {'form': form})


@grupo_required("admin")
def pacientes_excluir(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    if request.method == 'POST':
        paciente.delete()
        return redirect('pacientes_lista')

    return render(request, 'pacientes/excluir.html', {'paciente': paciente})



##### MEDICOS ####

@login_required
def medicos_lista(request):
    medicos = Medico.objects.all()
    return render(request, 'medicos/lista.html', {'medicos': medicos})


@login_required
def medicos_criar(request):
    form = MedicoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('medicos_lista')

    return render(request, 'medicos/form.html', {'form': form})


@login_required
def medicos_editar(request, id):
    medico = get_object_or_404(Medico, id=id)
    form = MedicoForm(request.POST or None, instance=medico)

    if form.is_valid():
        form.save()
        return redirect('medicos_lista')

    return render(request, 'medicos/form.html', {'form': form})


@grupo_required("admin")
def medicos_excluir(request, id):
    medico = get_object_or_404(Medico, id=id)

    if request.method == 'POST':
        medico.delete()
        return redirect('medicos_lista')

    return render(request, 'medicos/excluir.html', {'medico': medico})


#####CONSULTAS ####

@login_required
def consultas_agenda(request):
    consultas = Consulta.objects.select_related('paciente', 'medico').all()
    return render(request, 'consultas/agenda.html', {'consultas': consultas})


@login_required
def consultas_criar(request):
    form = ConsultaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('consultas_agenda')

    return render(request, 'consultas/form.html', {'form': form})


@login_required
def consultas_editar(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    form = ConsultaForm(request.POST or None, instance=consulta)

    if form.is_valid():
        form.save()
        return redirect('consultas_agenda')

    return render(request, 'consultas/form.html', {'form': form})


@grupo_required("admin")
def consultas_excluir(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    if request.method == 'POST':
        consulta.delete()
        return redirect('consultas_agenda')

    return render(request, 'consultas/excluir.html', {'consulta': consulta})

##### PAGAMENTOS ####

@grupo_required("Atendente")
def pagamentos_lista(request):
    pagamentos = Pagamento.objects.select_related(
        'consulta__paciente',
        'consulta__medico'
    )
    return render(request, 'pagamentos/lista.html', {'pagamentos': pagamentos})


@grupo_required("Atendente")
def pagamentos_criar(request):
    form = PagamentoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('pagamentos_lista')

    return render(request, 'pagamentos/form.html', {'form': form})


@grupo_required("Atendente")
def pagamentos_editar(request, id):
    pagamento = get_object_or_404(Pagamento, id=id)
    form = PagamentoForm(request.POST or None, instance=pagamento)

    if form.is_valid():
        form.save()
        return redirect('pagamentos_lista')

    return render(request, 'pagamentos/form.html', {'form': form})


@grupo_required("admin")
def pagamentos_excluir(request, id):
    pagamento = get_object_or_404(Pagamento, id=id)

    if request.method == 'POST':
        pagamento.delete()
        return redirect('pagamentos_lista')

    return render(request, 'pagamentos/excluir.html', {'pagamento': pagamento})

###### historico de pacientes #####
@login_required
def paciente_historico(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    consultas = Consulta.objects.filter(paciente=paciente).select_related('medico').prefetch_related('atendimento__exames').order_by('-data')

    pagamentos = Pagamento.objects.filter(consulta__paciente=paciente).select_related('consulta')

    total_gasto = pagamentos.filter(pago=True).aggregate(total=models.Sum('valor'))['total'] or 0

    return render(request, 'pacientes/historico.html', {
        'paciente': paciente,
        'consultas': consultas,
        'pagamentos': pagamentos,
        'total_gasto': total_gasto
    })

#####ATENDIMENTOS #####

@login_required
def atendimento_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    atendimento, created = Atendimento.objects.get_or_create(
        consulta=consulta
    )

    form = AtendimentoForm(request.POST or None, instance=atendimento)

    if form.is_valid():
        atendimento = form.save(commit=False)
        atendimento.consulta = consulta
        atendimento.save()
        atendimento.exames.clear()

        for exame in form.cleaned_data['exames']:
            AtendimentoExame.objects.create(
                atendimento=atendimento,
                exame=exame,
                status='solicitado'
            )

        return redirect('consultas_agenda')

    return render(request, 'atendimento/form.html', {
        'consulta': consulta,
        'form': form
    })

##### EXAMES #####

@login_required
def exames_lista(request):
    exames = Exame.objects.all()
    return render(request, 'exames/lista.html', {'exames': exames})

@login_required
def exames_criar(request):
    form = ExameForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('exames_lista')

    return render(request, 'exames/form.html', {'form': form})

@login_required
def exames_editar(request, id):
    exame = get_object_or_404(Exame, id=id)
    form = ExameForm(request.POST or None, instance=exame)

    if form.is_valid():
        form.save()
        return redirect('exames_lista')

    return render(request, 'exames/form.html', {'form': form})

@login_required
def exames_excluir(request, id):
    exame = get_object_or_404(Exame, id=id)

    if request.method == 'POST':
        exame.delete()
        return redirect('exames_lista')

    return render(request, 'exames/excluir.html', {'exame': exame})

@login_required
def atendimento_exame_status(request, id):
    exame_atendimento = get_object_or_404(AtendimentoExame, id=id)

    if request.method == 'POST':
        novo_status = request.POST.get('status')
        exame_atendimento.status = novo_status
        exame_atendimento.save()
        return redirect('paciente_historico', exame_atendimento.atendimento.consulta.paciente.id)

    return render(request, 'exames/status.html', {
        'exame_atendimento': exame_atendimento
    })
    

@login_required
def carregar_medicos(request):
    data = request.GET.get('data')

    medicos_lista = []

    if data:
        try:
            data_obj = datetime.strptime(data, '%Y-%m-%d')
            

            mapa = {
                0: 'segunda',
                1: 'terca',
                2: 'quarta',
                3: 'quinta',
                4: 'sexta',
                5: 'sabado',
            }

            dia_formatado = mapa.get(data_obj.weekday())

            if dia_formatado:
               
                for medico in Medico.objects.all():
                    if dia_formatado in medico.dias_atendimento:
                        medicos_lista.append({
                            'id': medico.id,
                            'nome': medico.nome
                        })

        except Exception as e:
            print("Erro:", e)

    return JsonResponse({'medicos': medicos_lista})