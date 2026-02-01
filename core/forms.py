
from django import forms
from .models import Paciente
from .models import HistoriaClinica

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombres', 'apellidos', 'cedula', 'telefono', 'direccion']
        widgets = {
            'cedula': forms.TextInput(attrs={
                'placeholder': 'Cédula',
                'pattern': '[0-9]+',
                'inputmode': 'numeric',
                'title': 'Ingrese solo números'
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Teléfono',
                'pattern': '[0-9]+',
                'inputmode': 'numeric',
                'title': 'Ingrese solo números'
            }),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula debe contener solo números")
        return cedula

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números")
        return telefono
    

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['tipo_terapia','sexo','diabetes','tipo_servicio','paciente_cama','paciente_silla','bipedestacion','control','trofismo','marcha','sensibilidad','tono_muscular','ama','tono_muscular','fuerza_muscular','reflejo','ef','paresia','plejia','lesion','signos','presion','sintomas','saturacion','fc','ap','af','alergias','qx','dm','tm','ei','el','peso','tf']


from django import forms
from .models import Tratamiento

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        exclude = ['paciente', 'fecha',]