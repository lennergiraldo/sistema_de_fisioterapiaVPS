from django.urls import path
from .views import mis_pacientes, login_view, buscar_paciente, editar_paciente, eliminar_paciente, historia_clinica,exportar_historia_pdf,tratamiento,tratamiento_pdf

urlpatterns = [
    path('', mis_pacientes, name='mis_pacientes'),
    path('login/', login_view, name='login'),
    path('buscar/',buscar_paciente, name='buscar_paciente'),
    path('editar/<int:paciente_id>/',editar_paciente, name='editar_paciente'),
    path('eliminar/<int:id>/',eliminar_paciente, name='eliminar_paciente'),
    path('historia/<int:paciente_id>/',historia_clinica, name='historia_clinica'),
   path('historia/<int:id>/pdf/', exportar_historia_pdf, name='exportar_historia_pdf'),
   path('tratamiento/<int:paciente_id>/',tratamiento, name='tratamiento'),
   
    path('tratamiento/pdf/<int:tratamiento_id>/',tratamiento_pdf, name='tratamiento_pdf'),
]

