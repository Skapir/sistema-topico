from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .apisnetpe import ApisNetPe
from topico.models.pacientes_models import Paciente
from topico.models.procedimientos_models import (
    TipoProcedimiento,
    Procedimiento,
    RegistroCuracionHerida,
    RegistroProcedimientoEspeciales,
    RegistroProcedimientoEspecifico,
    RegistroProcedimientoMedicos,
)
from topico.models.medicamentos_models import RegistroMedicamentos
from topico.models.materiales_insumos_models import RegistroMaterialesInsumos
from topico.models.diagnostico_medico_models import RegistroDiagnosticoMedico
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from itertools import chain
from django.core.paginator import Paginator
from weasyprint import HTML
from io import BytesIO
from django.http import HttpResponse
import time

api = ApisNetPe(token="apis-token-10976.ESTqxf6H2qYcVM0etJmR1fhGarzDVuKe")


@login_required
@csrf_exempt  # Esto es solo si tienes problemas con CSRF en AJAX
def optopico(request):
    # Código existente para cargar datos del paciente y renderizar la vista en caso de GET
    request.session.pop(
        "persona", None
    )  # Borra la clave "persona" de la sesión si existe

    persona = None
    busqueda_realizada = False

    if request.method == "POST":
        print("Datos recibidos en POST:", request.POST)  # Verifica qué datos llegan
        dni = request.POST.get("dni", "").strip()
        if not dni:
            dni = request.session.get("dni_paciente", "")
        print("DNI extraído:", dni)  # Verifica que el DNI no sea None ni vacío
        busqueda_realizada = True
        print("DNI buscado:", dni)

        if dni:
            # Guarda el DNI en la sesión para futuras consultas
            request.session["dni_paciente"] = dni

            start_time = time.time()  # Comienza a medir el tiempo antes de la consulta
            paciente_bd = Paciente.objects.filter(HI_NDOCUM=dni).first()
            print(
                "Paciente encontrado:", paciente_bd
            )  # Verifica si encuentra el paciente
            end_time = time.time()  # Termina de medir el tiempo después de la consulta
            tiempo_de_consulta = end_time - start_time  # Calcula el tiempo en segundos
            print(
                f"Tiempo de consulta en base de datos: {tiempo_de_consulta:.4f} segundos"
            )  # Muestra el tiempo en consola

            if paciente_bd:
                persona = {
                    "apellidoPaterno": (
                        paciente_bd.HI_NOMBRE.split()[0]
                        if paciente_bd.HI_NOMBRE
                        else ""
                    ),
                    "apellidoMaterno": (
                        paciente_bd.HI_NOMBRE.split()[1]
                        if len(paciente_bd.HI_NOMBRE.split()) > 1
                        else ""
                    ),
                    "nombres": " ".join(paciente_bd.HI_NOMBRE.split()[2:]),
                    "numeroDocumento": paciente_bd.HI_NDOCUM,
                    "direccion": paciente_bd.HI_DIRECC,
                    "estadoCivil": paciente_bd.HI_ESTCIV,
                    "sexo": paciente_bd.HI_SEXO,
                    "fechaNacimiento": paciente_bd.HI_FECNAC,
                    "historiaClinica": paciente_bd.HI_NREG,
                    "ubigeo": paciente_bd.HI_UBINAC,
                    "autogenerado": paciente_bd.HI_AUTASE,
                    "centro": paciente_bd.HI_CPOLIC,
                    "id": paciente_bd.id,
                    "id_personal": request.session.get("personal_id"),
                }
                request.session["persona"] = persona
            else:
                print("Paciente no encontrado en la BD.")
                # Si no se encuentra en la base de datos, consulta la API de RENIEC
                start_time_api = time.time()  # Inicia cronómetro para la API

                persona = api.get_person(dni)

                end_time_api = time.time()  # Termina cronómetro de la API
                tiempo_de_consulta_api = (
                    end_time_api - start_time_api
                )  # Tiempo de consulta API
                print(
                    f"Tiempo de consulta API RENIEC: {tiempo_de_consulta_api:.4f} segundos"
                )  # Muestra el tiempo en consola

                if persona:
                    request.session["persona"] = persona

    tipo_procedimiento_id = request.session.get("tipo_procedimiento_id")
    tipo_procedimiento = TipoProcedimiento.objects.all()

    context = {
        "persona": persona,
        "busqueda_realizada": busqueda_realizada,
        "tipo_procedimiento": tipo_procedimiento,
        "title": "Busqueda Paciente",
        "tipo_procedimiento_id": tipo_procedimiento_id,
    }

    return render(request, "op_topico/optopico.html", context)


@login_required
def rp_pacientes(request):
    # Contexto para enviar a la plantilla
    context = {
        "title": "Reporte de Pacientes",
        "user": request.user,
    }
    return render(request, "op_reportes/rp_pacientes.html", context)


@login_required
def c_pacientes(request):
    # Contexto para enviar a la plantilla
    context = {
        "title": "Consulta de Pacientes",
        "user": request.user,
    }
    return render(request, "op_consultas/c_pacientes.html", context)


@login_required
def consultar_atenciones_paciente(request):
    try:
        if request.method == "POST" or request.GET.get("page"):
            # Obtener parámetros del POST o GET
            dni_paciente = (
                request.POST.get("dni", "").strip()
                or request.GET.get("dni", "").strip()
            )
            tipo_procedimiento_id = (
                request.POST.get("tipo_procedimiento", "").strip()
                or request.GET.get("tipo_procedimiento", "").strip()
            )

            # Validación del DNI
            if not dni_paciente:
                messages.error(request, "⚠️ Por favor, ingrese un DNI.")
                return redirect("c_pacientes")

            if not dni_paciente.isdigit():
                messages.error(request, "⚠️ El DNI debe ser un número válido.")
                return redirect("c_pacientes")

            # Buscar paciente
            paciente = Paciente.objects.filter(HI_NDOCUM=dni_paciente).first()
            if not paciente:
                messages.error(
                    request, "⚠️ No se encontró un paciente con el DNI ingresado."
                )
                return redirect("c_pacientes")

            # Filtro por tipo de procedimiento
            filtro_procedimientos = Q()
            if tipo_procedimiento_id:
                filtro_procedimientos &= Q(tipo_procedimiento_id=tipo_procedimiento_id)

            # Obtener procedimientos por tipo
            procedimientos_generales = Procedimiento.objects.filter(
                Q(paciente=paciente) & filtro_procedimientos
            )
            for proc in procedimientos_generales:
                proc.tipo_procedimiento_nombre = "generales"

            procedimientos_especificos = RegistroProcedimientoEspecifico.objects.filter(
                Q(paciente=paciente) & filtro_procedimientos
            )

            for proc in procedimientos_especificos:
                proc.tipo_procedimiento_nombre = "especificos"
                proc.medicamentos = RegistroMedicamentos.objects.filter(
                    id_procedimiento_especifico=proc
                )
                proc.materiales = RegistroMaterialesInsumos.objects.filter(
                    id_procedimiento_especifico=proc
                )

            procedimientos_especiales = RegistroProcedimientoEspeciales.objects.filter(
                Q(paciente=paciente) & filtro_procedimientos
            )
            for proc in procedimientos_especiales:
                proc.tipo_procedimiento_nombre = "especiales"
                proc.materiales = RegistroMaterialesInsumos.objects.filter(
                    id_procedimiento_especiales=proc
                )

            procedimientos_medicos = RegistroProcedimientoMedicos.objects.filter(
                Q(paciente=paciente) & filtro_procedimientos
            )
            for proc in procedimientos_medicos:
                proc.tipo_procedimiento_nombre = "medicos"
                proc.materiales = RegistroMaterialesInsumos.objects.filter(
                    id_procedimiento_medico=proc
                )

            procedimientos_curaciones = RegistroCuracionHerida.objects.filter(
                Q(paciente=paciente) & filtro_procedimientos
            )
            for proc in procedimientos_curaciones:
                proc.tipo_procedimiento_nombre = "curacion_heridas"
                proc.materiales = RegistroMaterialesInsumos.objects.filter(
                    id_procedimiento_curacion=proc
                )
                proc.diagnostico = RegistroDiagnosticoMedico.objects.filter(
                    id_procedimiento_curacion=proc
                )

            # Combinar todas las atenciones
            atenciones = list(
                chain(
                    procedimientos_generales,
                    procedimientos_especificos,
                    procedimientos_especiales,
                    procedimientos_medicos,
                    procedimientos_curaciones,
                )
            )

            if not atenciones:
                messages.warning(
                    request,
                    f"⚠️ No se encontraron atenciones para el paciente {paciente.HI_NOMBRE}.",
                )
                return redirect("c_pacientes")

            # Ordenar por la fecha retornada por el método `get_fecha`
            atenciones.sort(key=lambda x: x.get_fecha(), reverse=True)

            # Paginación
            items_por_pagina = 20
            paginator = Paginator(atenciones, items_por_pagina)
            page_number = request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)

            # Estructura de paginación
            paginacion = {
                "current_page": page_number,
                "total_pages": paginator.num_pages,
                "has_previous": page_obj.has_previous(),
                "has_next": page_obj.has_next(),
                "previous_page": (
                    page_obj.previous_page_number() if page_obj.has_previous() else None
                ),
                "next_page": (
                    page_obj.next_page_number() if page_obj.has_next() else None
                ),
            }

            # Obtener tipos de procedimientos
            tipos_procedimiento = TipoProcedimiento.objects.all()

            context = {
                "title": "Atenciones de Pacientes",
                "paciente": paciente,
                "dni_paciente": dni_paciente,
                "atenciones": page_obj,
                "paginacion": paginacion,
                "tipos_procedimiento": tipos_procedimiento,
                "tipo_procedimiento_seleccionado": tipo_procedimiento_id,
            }
            return render(request, "op_consultas/c_pacientes.html", context)

    except Exception as e:
        # Captura de errores generales
        messages.error(request, f"❌ Error inesperado: {str(e)}")
        return redirect("c_pacientes")

    # Redirección si el método no es POST ni GET con 'page'
    return redirect("c_pacientes")


def generar_pdf_atencion(request, atencion_id, tipo_procedimiento):
    # Identificar el modelo según el tipo de procedimiento
    modelo_map = {
        "generales": Procedimiento,
        "especificos": RegistroProcedimientoEspecifico,
        "especiales": RegistroProcedimientoEspeciales,
        "medicos": RegistroProcedimientoMedicos,
        "curacion_heridas": RegistroCuracionHerida,
    }

    modelo = modelo_map.get(tipo_procedimiento.lower())
    if not modelo:
        return HttpResponse("Tipo de procedimiento no válido.", status=400)

    # Obtener el registro de atención
    atencion = get_object_or_404(modelo, id=atencion_id)

    # Obtener medicamentos si el tipo es ESPECIFICO
    medicamentos = None
    materiales = None
    diagnostico = None

    if tipo_procedimiento.lower() == "especificos":
        medicamentos = RegistroMedicamentos.objects.filter(
            id_procedimiento_especifico=atencion
        )
        materiales = RegistroMaterialesInsumos.objects.filter(
            id_procedimiento_especifico=atencion
        )

    # Obtener medicamentos si el tipo es ESPECIAL
    if tipo_procedimiento.lower() == "especiales":
        materiales = RegistroMaterialesInsumos.objects.filter(
            id_procedimiento_especiales=atencion
        )

    # Obtener medicamentos si el tipo es MEDICOS
    if tipo_procedimiento.lower() == "medicos":
        materiales = RegistroMaterialesInsumos.objects.filter(
            id_procedimiento_medico=atencion
        )
    # Obtener medicamentos si el tipo es CURACION HERIDAS
    if tipo_procedimiento.lower() == "curacion_heridas":
        materiales = RegistroMaterialesInsumos.objects.filter(
            id_procedimiento_curacion=atencion
        )
        diagnostico = RegistroDiagnosticoMedico.objects.filter(
            id_procedimiento_curacion=atencion
        )

    # Renderizar HTML del PDF
    context = {
        "atencion": atencion,
        "medicamentos": medicamentos,
        "materiales": materiales,
        "diagnostico": diagnostico,
    }
    html_string = render(request, "op_consultas/pdf_atencion.html", context).content
    html = HTML(string=html_string)

    # Generar el archivo PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="atencion_{atencion_id}.pdf"'
    html.write_pdf(response)

    return response
