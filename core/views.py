from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Paciente
from .forms import PacienteForm
from django.shortcuts import get_object_or_404, redirect
from .models import HistoriaClinica
from .forms import HistoriaClinicaForm
from django.http import HttpResponse
# ReportLab para generar PDFs
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from django.shortcuts import render, get_object_or_404
from .forms import TratamientoForm
from .models import Tratamiento

def login_view(request):
    """
    Vista de inicio de sesión
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mis_pacientes')
        else:
            return render(request, 'core/login.html', {
                'error': 'Usuario o contraseña incorrectos'
            })

    return render(request, 'core/login.html')



@login_required


@login_required
def mis_pacientes(request):
    """
    Vista principal donde se ingresan y listan los pacientes
    """
    pacientes = Paciente.objects.filter(medico=request.user)

    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.medico = request.user
            paciente.save()
            return redirect('mis_pacientes')
    else:
        form = PacienteForm()

    return render(request, 'core/mis_pacientes.html', {
        'form': form,
        'pacientes': pacientes
    })


def buscar_paciente(request):
    """
    Busca pacientes por número de CI
    """
    query = request.GET.get('cedula', '')

    pacientes = Paciente.objects.filter(
        medico=request.user,
        cedula__icontains=query
    )

    form = PacienteForm()

    return render(request, 'core/mis_pacientes.html', {
        'form': form,
        'pacientes': pacientes,
        'busqueda': query
    })


@login_required
def editar_paciente(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id, medico=request.user)

    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('mis_pacientes')
    else:
        form = PacienteForm(instance=paciente)

    pacientes = Paciente.objects.filter(medico=request.user)

    return render(request, 'core/mis_pacientes.html', {
        'form': form,
        'pacientes': pacientes,
        'editando': True,
        'paciente_id': paciente.id
    })



def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    paciente.delete()
    return redirect('mis_pacientes')


@login_required
def historia_clinica(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    historia, created = HistoriaClinica.objects.get_or_create(paciente=paciente)

    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST, instance=historia)
        if form.is_valid():
            form.save()
            return render(request, 'core/historia_clinica.html', {
                'form': form,
                'paciente': paciente,
                'historia': historia
            })
        
    else:
        form = HistoriaClinicaForm(instance=historia)

    return render(request, 'core/historia_clinica.html', {
        'form': form,
        'paciente': paciente,
        'historia': historia
    })




def exportar_historia_pdf(request, id):
    
    
    historia = HistoriaClinica.objects.get(id=id)
    paciente = historia.paciente

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historia_clinica_{paciente.nombres}_{paciente.apellidos}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50  # posición inicial

    # ---------- Función para manejar nueva página ----------
    def check_page(p, y, height, margen=50):
        if y < margen:
            p.showPage()
            y = height - 50
        return y
           
    # ---------- Funciones para campos ----------
    def campo_corto(p, y, etiqueta, valor):
        y = check_page(p, y, height)
        p.drawString(50, y, f"{etiqueta}:")
        p.drawString(400, y, f"{valor or 'No especificado'}")
        return y - 30

    def campo_largo(p, y, etiqueta, valor):
        y = check_page(p, y, height)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, f"{etiqueta}:")
        y -= 15
        p.setFont("Helvetica", 10)

        text_obj = p.beginText(50, y)
        text_obj.setLeading(14)

        texto = valor or "No especificado"
        for linea in texto.split("\n"):
            text_obj.textLine(linea)

        p.drawText(text_obj)
        y = text_obj.getY() - 20
        return y

    # ---------- MARCA DE AGUA ----------
    watermark_path = "core/static/images/marca_agua.png"
    try:
        watermark = ImageReader(watermark_path)
        p.saveState()
        p.setFillAlpha(0.12)
        p.drawImage(watermark, 100, 250, width=400, height=400, mask='auto')
        p.restoreState()
    except:
        pass
        
    # ====== ENCABEZADO ======
    p.setFont("Helvetica-Bold", 18)
    y = check_page(p, y, height)
    p.drawCentredString(width / 2, y, "INFORME DE HISTORIA CLÍNICA")
    y -= 30

    p.setFont("Helvetica", 10)
    y = check_page(p, y, height)
    p.drawCentredString(width / 2, y, "Centro de Rehabilitación Física")
    y -= 40

    # ====== SECCIÓN: DATOS DEL PACIENTE ======
    p.setFont("Helvetica-Bold", 12)
    y = check_page(p, y, height)
    p.drawString(50, y, "DATOS DEL PACIENTE")
    y -= 10
    p.line(50, y, width - 50, y)
    y -= 20

    p.setFont("Helvetica", 10)
    y = check_page(p, y, height)
    p.drawString(50, y, f"Nombres: {paciente.nombres}")
    p.drawString(300, y, f"Apellidos: {paciente.apellidos}")
    y -= 20

    y = check_page(p, y, height)
    p.drawString(50, y, f"Cédula: {paciente.cedula}")
    p.drawString(300, y, f"Teléfono: {paciente.telefono}")
    y -= 20

    y = check_page(p, y, height)
    p.drawString(50, y, f"Dirección: {paciente.direccion}")
    y -= 30
    
    y = check_page(p, y, height)
    p.drawString(50, y, f"SEXO: {historia.sexo or 'No especificado'}")
    y -= 30

    # ====== SECCIÓN: HISTORIA CLÍNICA ======
    p.setFont("Helvetica-Bold", 12)
    y = check_page(p, y, height)
    p.drawString(50, y, "EVALUACIÓN E INSPECCION")
    y -= 10
    p.line(50, y, width - 50, y)
    y -= 20

    p.setFont("Helvetica", 10)

    campos = [
        ("Tipo de Terapia", historia.tipo_terapia),
        ("DIABETES", historia.diabetes),
        ("TIPO DE SERVICIO", historia.tipo_servicio),
        ("PACIENTE EN CAMA", historia.paciente_cama),
        ("PACIENTE EN SILLA DE RUEDAS", historia.paciente_silla),
        ("BIPEDESTACIÓN", historia.bipedestacion),
        ("CONTROL DE ESFINTERES", historia.control),
        ("TROFISMO MUSCULAR", historia.trofismo),
        ("MARCHA", historia.marcha),
        ("MARCHA", historia.marcha),
        ("SENSIBILIDAD", historia.sensibilidad),
        ("TONO MUSCULAR", historia.tono_muscular),
        ("A.M.A", historia.ama),
        ("FUERZA MUSCULAR", historia.fuerza_muscular),
        ("REFLEJO", historia.reflejo),
        ("ESPASTICIDAD/FLACIDEZ", historia.ef),
        ("PLEJIA", historia.plejia),
        ("PARESIA", historia.paresia),
        ("SIGNOS", historia.signos),
        ("SINTOMAS", historia.sintomas),
        ("LESION", historia.lesion)
    ]

    for etiqueta, valor in campos:
        if etiqueta in ["SIGNOS", "SINTOMAS", "LESION"]:
            y = campo_largo(p, y, etiqueta, valor)
        else:
            y = campo_corto(p, y, etiqueta, valor)

    # ====== SECCIÓN: TRIAJE ======
    p.setFont("Helvetica-Bold", 12)
    y = check_page(p, y, height)
    p.drawString(50, y, "TRIAJE")
    y -= 10
    p.line(50, y, width - 50, y)
    y -= 20

    p.setFont("Helvetica", 10)

    campos = [
        ("PRESION ARTERIAL", historia.presion),
        ("SATURACION", historia.saturacion),
        ("FRECUENCIA CARDIACA", historia.fc),
        ("PESO", historia.peso),
        ("ANTECEDENTES PERSONALES", historia.ap),
        ("ANTECEDENTES FAMILIARES", historia.af),
        ("ALERGIAS", historia.alergias),
        ("QX", historia.qx),
        ("DIAGNOSTICO MEDICO", historia.dm),
        ("TRATAMIENTO FARMACO", historia.tf),
        ("TRATAMIENTO MÉDICO", historia.tm),
        ("ESTUDIOS DE IMAGEN", historia.ei),
        ("ESTUDIOS DE LABORATORIOS", historia.el),
    ]

    for etiqueta, valor in campos:
        if etiqueta in [
            "ANTECEDENTES PERSONALES",
            "ANTECEDENTES FAMILIARES",
            "ALERGIAS",
            "QX",
            "DIAGNOSTICO MEDICO",
            "TRATAMIENTO FARMACO",
            "TRATAMIENTO MÉDICO",
            "ESTUDIOS DE IMAGEN",
            "ESTUDIOS DE LABORATORIOS",
        ]:
            y = campo_largo(p, y, etiqueta, valor)
        else:
            y = campo_corto(p, y, etiqueta, valor)

    # ====== PIE DE PÁGINA ======
    p.setFont("Helvetica-Oblique", 9)
    y = check_page(p, y, height)
    p.drawCentredString(width / 2, 40, "Centro de Rehabilitación Física")

    p.showPage()
    p.save()
    return response

    #tratamiento 



def tratamiento(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    tratamiento = Tratamiento.objects.filter(paciente=paciente).first()

    if request.method == "POST":
        if tratamiento:
            form = TratamientoForm(request.POST, instance=tratamiento)
        else:
            form = TratamientoForm(request.POST)

        if form.is_valid():
            tratamiento = form.save(commit=False)
            tratamiento.paciente = paciente
            tratamiento.save()
    else:
        form = TratamientoForm(instance=tratamiento)

    return render(request, "core/tratamiento.html", {
        "paciente": paciente,
        "form": form
    })

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Tratamiento

def tratamiento_pdf(request, tratamiento_id):
    tratamiento = get_object_or_404(Tratamiento, id=tratamiento_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="tratamiento.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
        # ---------- MARCA DE AGUA ----------
    watermark_path = "core/static/images/marca_agua.png"
    try:
        watermark = ImageReader(watermark_path)
        p.saveState()
        p.setFillAlpha(0.12)
        p.drawImage(watermark, 100, 250, width=400, height=400, mask='auto')
        p.restoreState()
    except:
        pass
    # Título
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2, height - 50, "SEGUIMIENTO DEL ABORDAJE FISIOTERAPÉUTICO")


    p.setFont("Helvetica", 10)

    p.drawString(50, height - 100, f"Paciente: {tratamiento.paciente.nombres} {tratamiento.paciente.apellidos}")
    p.drawString(300, height - 100, f"CI: {tratamiento.paciente.cedula}")
    
    p.drawString(50, height - 120, f"N° Sesión: {tratamiento.numero_sesion}")
    p.drawString(50, height - 140, f"EVA Inicial: {tratamiento.eva_inicial}")
    p.drawString(300, height - 140, f"EVA Final: {tratamiento.eva_final}")

    # PROFESIONAL / Firma
    p.drawString(300, height - 120, f"PROFESIONAL: {tratamiento.firma_tm or 'No registrada'}")

    y = height - 180

    # Observaciones
    p.drawString(50, y, "FASE DE RECUPERACIÓN 1:")
    y -= 20
    for linea in tratamiento.observaciones.split('\n'):
        p.drawString(60, y, linea)
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50

    y -= 10
    # Recomendaciones
    p.drawString(50, y, "FASE DE RECUPERACIÓN 2:")
    y -= 20
    for linea in tratamiento.recomendaciones.split('\n'):
        p.drawString(60, y, linea)
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50

    p.drawString(50, y, "FASE DE RECUPERACIÓN 3:")
    y -= 20
    for linea in tratamiento.fase3.split('\n'):
        p.drawString(60, y, linea)
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50

    p.drawString(50, y, "FASE DE RECUPERACIÓN 4:")
    y -= 20
    for linea in tratamiento.fase4.split('\n'):
        p.drawString(60, y, linea)
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50







    y -= 10
    # Agentes Electroterapéuticos
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "APARATOLOGÍA")
    y -= 10
    p.line(50, y, width - 50, y)
    y -= 20
    p.setFont("Helvetica", 10)
    p.drawString(50, y, "Agentes Electroterapéuticos:")
    y -= 20

    check_fields = [
        ("CHC", tratamiento.chc),
        ("CHF", tratamiento.chf),
        ("US", tratamiento.us),
        ("Infrarrojo", tratamiento.infrarrojo),
        ("Magneto", tratamiento.magneto),
        ("Electrodos", tratamiento.electrodos),
        ("Láser", tratamiento.laser),
        ("Onda de choque", tratamiento.onda_choque),
        ("Punción seca", tratamiento.puncion_seca),
        ("Terapia manual", tratamiento.terapia_manual),
    ]

    for nombre, valor in check_fields:
        status = "Sí" if valor else "No"  # muestra si está marcado
        p.drawString(60, y, f"- {nombre}: {status}")
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 300
  

    p.showPage()
    p.save()
    return response