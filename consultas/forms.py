from django import forms
from .models import Paciente, Medico,Consulta, Pagamento, Atendimento, Exame
from datetime import datetime


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'telefone']

class MedicoForm(forms.ModelForm):

    dias_atendimento = forms.MultipleChoiceField(
        choices=Medico.DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Medico
        fields = ['nome', 'crm', 'telefone', 'especialidade', 'dias_atendimento']

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['data', 'paciente', 'medico']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.fields['medico'].queryset = Medico.objects.none()

        
        if 'data' in self.data:
            try:
                data_obj = datetime.strptime(
                    self.data.get('data'),
                    '%Y-%m-%d'
                )


                mapa = {
                    0: 'segunda',
                    1: 'terca',
                    2: 'quarta',
                    3: 'quinta',
                    4: 'sexta',
                    5: 'sabado',
                    6: 'domingo',
                }

                dia_formatado = mapa.get(data_obj.weekday())

                medicos_disponiveis = []
                
                for medico in Medico.objects.all():
                    if dia_formatado in medico.dias_atendimento:
                        medicos_disponiveis.append(medico.id)

                self.fields['medico'].queryset = Medico.objects.filter(id__in=medicos_disponiveis)

            except (ValueError, TypeError):
                pass    

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['consulta', 'valor', 'data_pagamento', 'forma_pagamento', 'pago']
        widgets = {
            'data_pagamento': forms.DateInput(attrs={'type': 'date'})
        }

class AtendimentoForm(forms.ModelForm):
    exames = forms.ModelMultipleChoiceField(
        queryset=Exame.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Atendimento
        fields = ['descricao', 'exames']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
            'exames': forms.CheckboxSelectMultiple()
        }

class ExameForm(forms.ModelForm):
    class Meta:
        model = Exame
        fields = ['nome','valor']