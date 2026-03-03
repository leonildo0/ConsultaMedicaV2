from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
   

    path('', views.dashboard, name='dashboard'), 
    ##### PACIENTES ####
    path('pacientes/', views.pacientes_lista, name='pacientes_lista'),
    path('pacientes/novo/', views.pacientes_criar, name='pacientes_criar'),
    path('pacientes/<int:id>/editar/', views.pacientes_editar, name='pacientes_editar'),
    path('pacientes/<int:id>/excluir/', views.pacientes_excluir, name='pacientes_excluir'),
    #### historico de pacientes #####
    path('<int:id>/historico/', views.paciente_historico, name='paciente_historico'),


    ##### MEDICOS ####
   path('medicos/', views.medicos_lista, name='medicos_lista'),
    path('medicos/novo/', views.medicos_criar, name='medicos_criar'),
    path('medicos/<int:id>/editar/', views.medicos_editar, name='medicos_editar'),
    path('medicos/<int:id>/excluir/', views.medicos_excluir, name='medicos_excluir'),

    #####CONSULTAS ####
    path('consultas/', views.consultas_agenda, name='consultas_agenda'),
    path('consultas/nova/', views.consultas_criar, name='consultas_criar'),
    path('consultas/<int:id>/editar/', views.consultas_editar, name='consultas_editar'),
    path('consultas/<int:id>/excluir/', views.consultas_excluir, name='consultas_excluir'),
    
    ##### PAGAMENTOS ####
    path('pagamentos/', views.pagamentos_lista, name='pagamentos_lista'),
    path('pagamentos/novo/', views.pagamentos_criar, name='pagamentos_criar'),
    path('pagamentos/<int:id>/editar/', views.pagamentos_editar, name='pagamentos_editar'),
    path('pagamentos/<int:id>/excluir/', views.pagamentos_excluir, name='pagamentos_excluir'),

    ######ATENDIMENTOS #####
    path('consultas/<int:consulta_id>/atendimento/',views.atendimento_consulta,name='atendimento_consulta'),

    ###### EXAMES #####
    path('exames/', views.exames_lista, name='exames_lista'),
    path('exames/novo/', views.exames_criar, name='exames_criar'),
    path('exames/<int:id>/editar/', views.exames_editar, name='exames_editar'),
    path('exames/<int:id>/excluir/', views.exames_excluir, name='exames_excluir'),
    path('atendimento/exame/<int:id>/status/',views.atendimento_exame_status,name='atendimento_exame_status'),

    ### AJAX para carregar medicos######
    path('ajax/carregar-medicos/', views.carregar_medicos, name='carregar_medicos'),

]
