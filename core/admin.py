

# Register your models here.
from django.contrib import admin
from .models import Paciente
from .models import HistoriaClinica

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'medico')

   

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'sexo','tipo_terapia','lesion')