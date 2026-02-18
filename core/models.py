

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    medico = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pacientes'
    )

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} {self.cedula}"
    
class HistoriaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)

    TIPO_TERAPIA_CHOICES = [
        ('pediatria', 'Pediatría'),
        ('traumatologia', 'Traumatología'),
        ('neurologia', 'Neurología'),
        ('geriatria', 'Geriatría'),
        ('deportiva', 'Deportiva'),
    ]
    SEXO_CHOICES = [
        ('MASCULINO', 'MASCULINO'),
        ('FEMENINO', 'FEMENINO'),
        ]
    DIABETES_CHOICES = [
        ('SI', 'SI'),
        ('NO', 'NO'),
        ]
    TIPO_SERVICIO_CHOICES = [
        ('DOMICILIO', 'DOMICILIO'),
        ('CONSULTORIO', 'CONSULTORIO'),
        ]
    PACIENTE_CAMA_CHOICES = [
        ('SI', 'SI'),
        ('NO', 'NO'),
        ]
    PACIENTE_SILLA_CHOICES = [
        ('SI', 'SI'),
        ('NO', 'NO'),
        ]
    BIPEDESTACION_CHOICES = [
        ('SI CON APOYO', 'SI CON APOYO'),
        ('SI SIN APOYO', 'SI SIN APOYO'),
        ('NO', 'NO'),
        ]
    CONTROL_CHOICES = [
        ('SI', 'SI'),
        ('NO', 'NO'),
        ]
    
    TROFISMO_CHOICES = [
        ('NORMAL', 'NORMAL'),
        ('HIPOTROFISMO', 'HIPOTROFISMO'),
        ('HIPERTROFISMO', 'HIPERTROFISMO'),
        ]
    MARCHA_CHOICES = [
        ('INDEPENDIENTE', 'INDEPENDIENTE'),
        ('MULETA', 'MULETA'),
        ('ANDADOR', 'ANDADOR'),
        ('BASTÓN', 'BASTÓN'),
        ('OTRO', 'OTRO'),
        ('NO', 'NO'),
        ]
    SENSIBILIDAD_CHOICES = [
        ('PRESENTE', 'PRESENTE'),
        ('AUSENTE', 'AUSENTE'),
        ]
    TONO_MUSCULAR_CHOICES = [
        ('NORMOTONO', 'NORMOTONO'),
        ('HIPERTÓNICO', 'HIPERTÓNICO'),
        ('HIPOTÓNICO', 'HIPOTÓNICO'),
        ]
    AMA_CHOICES = [
        ('CODO', 'CODO'),
        ('RODILLA', 'RODILLA'),
        ('HOMBRO', 'HOMBRO'),
        ('TOBILLO', 'TOBILLO'),
        ('CADERA', 'CADERA'),
        ('MUÑECA', 'MUÑECA'),
        ('METACARPO FALANGICAS', 'METACARPO FALANGICAS'),
        ('FALANGE MEDIA', 'FALANGE MEDIA'),
        ('FALANGE DISTAL', 'FALANGE DISTAL'),
        ('MATATARSOFALANGICAS', 'MATATARSOFALANGICAS'),
        ('CERVICAL', 'CERVICAL'),
        ]
    
    FUERZA_CHOICES = [
        ('UNO', 'UNO'),
        ('DOS', 'DOS'),
        ('TRES', 'TRES'),
        ('CUATRO', 'CUATRO'),
        ('CINCO', 'CINCO'),
        ]
    REFLEJO_CHOICES = [
        ('AUSENTE', 'AUSENTE'),
        ('PRESENTE', 'PRESENTE'),
        ]
    EF_CHOICES = [
        ('ESPASTICIDAD', 'ESPASTICIDAD'),
        ('FLACIDEZ', 'FLACIDEZ'),
        ]
    PLEJIA_CHOICES = [
        ('CUADRIPLEJIA', 'CUADRIPLEJIA'),
        ('TETRAPLEJIA', 'TETRAPLEJIA'),
        ('MONOPLEJIA', 'MONOPLEJIA'),
        ('HOMOPLEJIA', 'HOMOPLEJIA'),
        ('PARAPLEJIA', 'PARAPLEJIA'),
        ('TRIPLEJIA', 'TRIPLEJIA'),
        ('DIPLEJIA', 'DIPLEJIA'),
        ('NO', 'NO'),
        ]
    PARESIA_CHOICES = [
        ('CUADRIPERESIA', 'CUADRIPERESIA'),
        ('TETRAPARESIA', 'TETRAPARESIA'),
        ('HEMIPARESIA', 'HEMIPARESIA'),
        ('MONOPARESIA', 'MONOPARESIA'),
        ('PARAPARESIA', 'PARAPARESIA'),
        ('TRIPARESIA', 'TRIPARESIA'),
        ('DIPARESIA', 'DIPARESIA'),
        ('NO', 'NO'),
        ]
    
    

    tipo_terapia = models.CharField(max_length=20, choices=TIPO_TERAPIA_CHOICES, blank=True, null=True)
    sexo = models.CharField(max_length=20, choices=SEXO_CHOICES, blank=True, null=True)
    diabetes = models.CharField(max_length=20, choices=DIABETES_CHOICES, blank=True, null=True)
    tipo_servicio= models.CharField(max_length=20, choices=TIPO_SERVICIO_CHOICES, blank=True, null=True)
    paciente_cama = models.CharField(max_length=20, choices=PACIENTE_CAMA_CHOICES, blank=True, null=True)
    paciente_silla = models.CharField(max_length=20, choices=PACIENTE_SILLA_CHOICES, blank=True, null=True)
    bipedestacion = models.CharField(max_length=20, choices=BIPEDESTACION_CHOICES, blank=True, null=True)
    control = models.CharField(max_length=20, choices=CONTROL_CHOICES, blank=True, null=True)
    trofismo = models.CharField(max_length=20, choices=TROFISMO_CHOICES, blank=True, null=True)
    marcha = models.CharField(max_length=20, choices=MARCHA_CHOICES, blank=True, null=True)
    sensibilidad = models.CharField(max_length=20, choices=SENSIBILIDAD_CHOICES, blank=True, null=True)
    tono_muscular = models.CharField(max_length=20, choices=TONO_MUSCULAR_CHOICES, blank=True, null=True)
    ama = models.CharField(max_length=20, choices=AMA_CHOICES, blank=True, null=True)
    fuerza_muscular = models.CharField(max_length=20, choices=FUERZA_CHOICES, blank=True, null=True)
    reflejo = models.CharField(max_length=20, choices=REFLEJO_CHOICES, blank=True, null=True)
    ef = models.CharField(max_length=20, choices=EF_CHOICES, blank=True, null=True)
    plejia = models.CharField(max_length=20, choices=PLEJIA_CHOICES, blank=True, null=True)
    paresia = models.CharField(max_length=20, choices=PARESIA_CHOICES, blank=True, null=True)
    
    sintomas = models.TextField(null=True, blank=True)
    signos = models.TextField(null=True, blank=True)
    
    lesion = models.TextField(null=True, blank=True)
    ap= models.TextField(null=True, blank=True)
    af= models.TextField(null=True, blank=True)
    dm= models.TextField(null=True, blank=True)
    ei= models.TextField(null=True, blank=True)
    el= models.TextField(null=True, blank=True)
    qx= models.TextField(null=True, blank=True)
    tm= models.TextField(null=True, blank=True)
    tf= models.TextField(null=True, blank=True)
    alergias= models.TextField(null=True, blank=True)
    saturacion = models.CharField(max_length=100, null=True, blank=True)
    fc = models.CharField(max_length=100, null=True, blank=True)
    peso= models.CharField(max_length=100, null=True, blank=True)
    presion = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return f"Historia clínica de {self.paciente.nombres} {self.paciente.apellidos}"
    

    #tratamiento 

class Tratamiento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='tratamientos')
    fecha = models.DateField(auto_now_add=True)
    numero_sesion = models.PositiveIntegerField()
    eva_inicial = models.CharField(max_length=10, blank=True)
    eva_final = models.CharField(max_length=10, blank=True)
    observaciones = models.TextField(blank=True)
    recomendaciones = models.TextField(blank=True)
    fase3 = models.TextField(blank=True)
    fase4 = models.TextField(blank=True)



    # Agentes
    chc = models.BooleanField(default=False)
    chf = models.BooleanField(default=False)
    us = models.BooleanField(default=False)
    infrarrojo = models.BooleanField(default=False)
    magneto = models.BooleanField(default=False)
    electrodos = models.BooleanField(default=False)
    laser = models.BooleanField(default=False)
    onda_choque = models.BooleanField(default=False)
    puncion_seca = models.BooleanField(default=False)
    terapia_manual = models.BooleanField(default=False)

    # Firma
    firma_tm = models.CharField(max_length=150, blank=True)

    def _str_(self):
        return f"Historia clínica de {self.paciente.nombres} {self.paciente.apellidos} {self.paciente.cedula}"
    


from django.db import models
from django.utils import timezone

class Contabilidad(models.Model):

    TIPO_CHOICES = (
        ('deuda', 'Deuda (Terapia)'),
        ('pago', 'Pago'),
        ('anticipo', 'Pago Anticipado'),
    )

    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='movimientos')
    fecha = models.DateField(default=timezone.now)
    descripcion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    creado = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.paciente} - {self.tipo} - {self.monto}"