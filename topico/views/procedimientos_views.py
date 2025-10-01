from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from ..models import (
    Procedimiento,
    TipoProcedimiento,
    RegistroProcedimientoEspecifico,
    RegistroMedicamentos,
    Medicamentos,
    MaterialesInsumos,
    RegistroMaterialesInsumos,
    RegistroProcedimientoEspeciales,
    RegistroProcedimientoMedicos,
    DiagnosticoMedico,
    RegistroDiagnosticoMedico,
    RegistroCuracionHerida,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponse
from itertools import chain
from xhtml2pdf import pisa
import pandas as pd
from django.template.loader import render_to_string
from datetime import datetime


@login_required
def r_procedimientos(request):
    # Contexto para enviar a la plantilla
    persona = request.session.get("persona", None)
    context = {"title": "Procedimiento", "persona": persona}
    return render(request, "op_topico/r_procedimientos.html", context)


@login_required
def rp_procedimientos(request):
    responsables = User.objects.filter(is_active=True)
    procedimientos = []

    if request.method == "POST":
        # Obtener los valores del formulario
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        tipo_procedimiento_id = request.POST.get("tipo_procedimiento")
        responsable_id = request.POST.get("responsable")

        # Filtros para cada modelo
        filtros_generales = Q()
        filtros_especificos = Q()
        filtros_especiales = Q()
        filtros_medicos = Q()
        filtros_curacion = Q()

        if fecha_inicio:
            filtros_generales &= Q(fecha_registro__gte=fecha_inicio)
            filtros_especificos &= Q(fecha_registro__gte=fecha_inicio)
            filtros_especiales &= Q(fecha_registro__gte=fecha_inicio)
            filtros_medicos &= Q(fecha_registro__gte=fecha_inicio)
            filtros_curacion &= Q(fecha_registro__gte=fecha_inicio)
        if fecha_fin:
            filtros_generales &= Q(fecha_registro__lte=fecha_fin)
            filtros_especificos &= Q(fecha_registro__lte=fecha_fin)
            filtros_especiales &= Q(fecha_registro__lte=fecha_fin)
            filtros_medicos &= Q(fecha_registro__lte=fecha_fin)
            filtros_curacion &= Q(fecha_registro__lte=fecha_fin)
        if tipo_procedimiento_id:
            filtros_generales &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
            filtros_especificos &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
            filtros_especiales &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
            filtros_medicos &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
            filtros_curacion &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
        if responsable_id:
            filtros_generales &= Q(personal_id=responsable_id)
            filtros_especificos &= Q(personal_id=responsable_id)
            filtros_especiales &= Q(personal_id=responsable_id)
            filtros_medicos &= Q(personal_id=responsable_id)
            filtros_curacion &= Q(personal_id=responsable_id)

        # Consultas para cada modelo
        procedimientos_generales = Procedimiento.objects.filter(filtros_generales)
        procedimientos_especificos = RegistroProcedimientoEspecifico.objects.filter(
            filtros_especificos
        )
        procedimientos_especiales = RegistroProcedimientoEspeciales.objects.filter(
            filtros_especiales
        )
        procedimientos_medicos = RegistroProcedimientoMedicos.objects.filter(
            filtros_medicos
        )
        procedimientos_curacion = RegistroCuracionHerida.objects.filter(
            filtros_curacion
        )

        # Combinar los procedimientos
        procedimientos = chain(
            procedimientos_generales,
            procedimientos_especificos,
            procedimientos_especiales,
            procedimientos_medicos,
            procedimientos_curacion,
        )

    context = {
        "title": "Reporte de Procedimientos",
        "tipos_procedimientos": TipoProcedimiento.objects.all(),
        "user": request.user,
        "responsables": responsables,
        "procedimientos": procedimientos,  # Pasar todos los procedimientos al contexto
    }
    return render(request, "op_reportes/rp_procedimientos.html", context)


@login_required
def export_procedimientos_excel(request):
    # Recolectar los procedimientos según los filtros actuales
    responsables = User.objects.filter(is_active=True)
    procedimientos = []

    # Filtros de búsqueda
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    tipo_procedimiento_id = request.GET.get("tipo_procedimiento")
    responsable_id = request.GET.get("responsable")

    filtros_generales = Q()
    filtros_especificos = Q()
    filtros_especiales = Q()
    filtros_medicos = Q()
    filtros_curacion = Q()

    if fecha_inicio:
        filtros_generales &= Q(fecha_registro__gte=fecha_inicio)
        filtros_especificos &= Q(fecha_registro__gte=fecha_inicio)
        filtros_especiales &= Q(fecha_registro__gte=fecha_inicio)
        filtros_medicos &= Q(fecha_registro__gte=fecha_inicio)
        filtros_curacion &= Q(fecha_registro__gte=fecha_inicio)
    if fecha_fin:
        filtros_generales &= Q(fecha_registro__lte=fecha_fin)
        filtros_especificos &= Q(fecha_registro__lte=fecha_fin)
        filtros_especiales &= Q(fecha_registro__lte=fecha_fin)
        filtros_medicos &= Q(fecha_registro__lte=fecha_fin)
        filtros_curacion &= Q(fecha_registro__lte=fecha_fin)
    if tipo_procedimiento_id:
        filtros_generales &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
        filtros_especificos &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
        filtros_especiales &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
        filtros_medicos &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
        filtros_curacion &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
    if responsable_id:
        filtros_generales &= Q(personal_id=responsable_id)
        filtros_especificos &= Q(personal_id=responsable_id)
        filtros_especiales &= Q(personal_id=responsable_id)
        filtros_medicos &= Q(personal_id=responsable_id)
        filtros_curacion &= Q(personal_id=responsable_id)

    # Consultar cada modelo
    procedimientos_generales = Procedimiento.objects.filter(filtros_generales)
    procedimientos_especificos = RegistroProcedimientoEspecifico.objects.filter(
        filtros_especificos
    )
    procedimientos_especiales = RegistroProcedimientoEspeciales.objects.filter(
        filtros_especiales
    )
    procedimientos_medicos = RegistroProcedimientoMedicos.objects.filter(
        filtros_medicos
    )
    procedimientos_curacion = RegistroCuracionHerida.objects.filter(filtros_curacion)

    # Combinar
    procedimientos = chain(
        procedimientos_generales,
        procedimientos_especificos,
        procedimientos_especiales,
        procedimientos_medicos,
        procedimientos_curacion,
    )

    # Crear un DataFrame
    data = [
        {
            "Fecha": proc.fecha_registro,
            "Paciente": (
                proc.paciente.HI_NOMBRE
                if hasattr(proc.paciente, "HI_NOMBRE")
                else "N/A"
            ),
            "Tipo de Procedimiento": (
                proc.tipo_procedimiento.descripcion
                if proc.tipo_procedimiento
                else "N/A"
            ),
            "Responsable": (
                proc.personal.username if hasattr(proc.personal, "username") else "N/A"
            ),
        }
        for proc in procedimientos
    ]
    df = pd.DataFrame(data)

    # Crear el archivo Excel
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="procedimientos.xlsx"'
    with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Procedimientos")
    return response


@login_required
def export_procedimientos_pdf(request):
    # Recolectar los procedimientos según los filtros actuales
    responsables = User.objects.filter(is_active=True)
    procedimientos = []

    # Filtros de búsqueda (idénticos al Excel)
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    tipo_procedimiento_id = request.GET.get("tipo_procedimiento")
    responsable_id = request.GET.get("responsable")

    filtros_generales = Q()
    filtros_especificos = Q()
    filtros_especiales = Q()
    filtros_medicos = Q()
    filtros_curacion = Q()

    if fecha_inicio:
        filtros_generales &= Q(fecha_registro__gte=fecha_inicio)
        filtros_especificos &= Q(fecha_registro__gte=fecha_inicio)
        filtros_especiales &= Q(fecha_registro__gte=fecha_inicio)
        filtros_medicos &= Q(fecha_registro__gte=fecha_inicio)
        filtros_curacion &= Q(fecha_registro__gte=fecha_inicio)
    if fecha_fin:
        filtros_generales &= Q(fecha_registro__lte=fecha_fin)
        filtros_especificos &= Q(fecha_registro__lte=fecha_fin)
        filtros_especiales &= Q(fecha_registro__lte=fecha_fin)
        filtros_medicos &= Q(fecha_registro__lte=fecha_fin)
        filtros_curacion &= Q(fecha_registro__lte=fecha_fin)
    if tipo_procedimiento_id:
        filtros_generales &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
        filtros_especificos &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
        filtros_especiales &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
        filtros_medicos &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
        filtros_curacion &= Q(tipo_procedimiento_id=tipo_procedimiento_id)
    if responsable_id:
        filtros_generales &= Q(personal_id=responsable_id)
        filtros_especificos &= Q(personal_id=responsable_id)
        filtros_especiales &= Q(personal_id=responsable_id)
        filtros_medicos &= Q(personal_id=responsable_id)
        filtros_curacion &= Q(personal_id=responsable_id)

    procedimientos_generales = Procedimiento.objects.filter(filtros_generales)
    procedimientos_especificos = RegistroProcedimientoEspecifico.objects.filter(
        filtros_especificos
    )
    procedimientos_especiales = RegistroProcedimientoEspeciales.objects.filter(
        filtros_especiales
    )
    procedimientos_medicos = RegistroProcedimientoMedicos.objects.filter(
        filtros_medicos
    )
    procedimientos_curacion = RegistroCuracionHerida.objects.filter(filtros_curacion)

    procedimientos = chain(
        procedimientos_generales,
        procedimientos_especificos,
        procedimientos_especiales,
        procedimientos_medicos,
        procedimientos_curacion,
    )

    # Renderizar el HTML del PDF
    context = {
        "procedimientos": procedimientos,
        "fecha_actual": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }
    html = render_to_string("op_reportes/procedimientos_pdf.html", context)

    # Generar el PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="procedimientos.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    return response


@login_required
def r_procedimientos_generales(request):
    if request.method == "POST":
        # Obtener datos del formulario
        data = request.POST
        observacion = data.get("observacion", "")
        presion_arterial = data.get("presion_arterial")
        temperatura = data.get("temperatura")
        frecuencia_cardiaca = data.get("frecuencia_cardiaca")
        saturacion_oxigeno = data.get("saturacion_oxigeno")
        volumen_oxigeno = data.get("volumen_oxigeno")

        # Recuperar ID de paciente y tipo de procedimiento desde la sesión
        persona = request.session.get("persona", None)
        tipo_procedimiento_id = request.session.get("tipo_procedimiento_id")
        personal_id = request.session.get("personal_id")

        # Verificar que los datos esenciales estén disponibles
        if not persona or not tipo_procedimiento_id or not personal_id:
            messages.error(request, "Datos incompletos en la sesión")
            return redirect("r_procedimientos_generales")

        try:
            personal = User.objects.get(id=personal_id)
            tipo_procedimiento = TipoProcedimiento.objects.get(id=tipo_procedimiento_id)

            # Crear el procedimiento en la base de datos
            Procedimiento.objects.create(
                fecha_registro=timezone.now(),
                observacion=observacion,
                tipo_procedimiento=tipo_procedimiento,
                personal=personal,
                paciente_id=persona["id"],
                presion_arterial=presion_arterial,
                temperatura=temperatura,
                frecuencia_cardiaca=frecuencia_cardiaca,
                saturacion_oxigeno=saturacion_oxigeno,
                volumen_oxigeno=volumen_oxigeno,
            )

            # Limpiar los datos de la sesión
            request.session.pop("tipo_procedimiento_id", None)

            # Añadir mensaje de éxito
            messages.success(request, "Procedimiento registrado con éxito")
            return redirect("r_procedimientos_generales")

        except Exception as e:
            messages.error(request, "Error al guardar el procedimiento")
            print("Error al guardar el procedimiento:", e)
            return redirect("r_procedimientos_generales")

    # Si es una solicitud GET, cargar el contexto necesario para la plantilla
    tipo_procedimiento_id = request.session.get("tipo_procedimiento_id")

    context = {
        "title": "Registro de Procedimiento General",
        "persona": request.session.get("persona", None),
        "tipo_procedimiento_id": tipo_procedimiento_id,
    }
    return render(
        request, "op_topico/registros_procedimientos/proc_generales.html", context
    )


@login_required
def r_procedimientos_especificos(request):
    if request.method == "POST":
        print("Datos recibidos en request.POST:", request.POST)

        # Obtener datos del formulario
        descripcion = request.POST.get("descripcion", "").strip()
        materiales = list(set(request.POST.getlist("materiales[]")))
        cantidades_materiales = request.POST.getlist("cantidades_materiales[]")
        medicamentos = list(set(request.POST.getlist("medicamentos[]")))

        # Validar datos del formulario
        if not descripcion:
            print("⚠️ Error: No se proporcionó una descripción para el procedimiento.")
        else:
            print(f"✅ Descripción del procedimiento: {descripcion}")

        if not materiales:
            print("⚠️ Error: No se recibieron materiales.")
        else:
            print(f"✅ Materiales seleccionados: {materiales}")

        if not cantidades_materiales:
            print("⚠️ Error: No se recibieron cantidades de materiales.")
        else:
            print(f"✅ Cantidades de materiales: {cantidades_materiales}")

        if not medicamentos:
            print("⚠️ Error: No se recibieron medicamentos.")
        else:
            print(f"✅ Medicamentos seleccionados: {medicamentos}")

        # Recuperar datos de sesión
        paciente = request.session.get("persona")
        tipo_procedimiento_id = request.session.get("tipo_procedimiento_id")
        personal_id = request.session.get("personal_id")

        print(f"Paciente en sesión: {paciente}")
        print(f"Tipo de procedimiento en sesión: {tipo_procedimiento_id}")
        print(f"Personal logueado: {personal_id}")

        # Validar datos obligatorios de la sesión
        if not paciente or not tipo_procedimiento_id or not personal_id:
            messages.error(
                request, "⚠️ Datos incompletos en la sesión. Por favor, verifica."
            )
            return redirect("r_procedimientos_especificos")

        try:
            # Recuperar instancias necesarias
            personal = User.objects.get(id=personal_id)
            tipo_procedimiento = TipoProcedimiento.objects.get(id=tipo_procedimiento_id)

            with transaction.atomic():
                # Registrar procedimiento específico
                procedimiento = RegistroProcedimientoEspecifico.objects.create(
                    fecha_registro=now(),
                    descripcion=descripcion,
                    paciente_id=paciente["id"],
                    personal=personal,
                    tipo_procedimiento=tipo_procedimiento,
                )
                print(
                    f"✅ Procedimiento específico registrado con ID: {procedimiento.id}"
                )

                # Procesar materiales asociados
                for material_id, cantidad in zip(materiales, cantidades_materiales):
                    cantidad = int(cantidad)
                    material = MaterialesInsumos.objects.get(id=material_id)

                    # Validar stock disponible
                    if material.stock_actual < cantidad:
                        raise ValueError(
                            f"Stock insuficiente para el material '{material.descripcion}'. Disponible: {material.stock_actual}, Requerido: {cantidad}."
                        )

                    # Registrar la salida en el modelo RegistroMaterialesInsumos
                    RegistroMaterialesInsumos.objects.create(
                        materiales_insumos=material,
                        tipo_movimiento="salida",
                        cantidad=cantidad,
                        personal=personal,
                        paciente_id=paciente["id"],
                        tipo_procedimiento=tipo_procedimiento,
                        fecha_registro=now(),
                        id_procedimiento_especifico=procedimiento,
                    )
                    print(
                        f"✅ Salida registrada para material '{material.descripcion}' - Cantidad: {cantidad}"
                    )

                    # Actualizar stock del material
                    material.stock_actual -= cantidad
                    material.save()
                    print(
                        f"🔄 Stock actualizado para '{material.descripcion}': {material.stock_actual}"
                    )

                # Registrar medicamentos asociados
                for medicamento_id in medicamentos:
                    medicamento = Medicamentos.objects.get(id=medicamento_id)

                    # Registrar el medicamento en la tabla correspondiente
                    RegistroMedicamentos.objects.create(
                        medicamentos_id=medicamento.id,
                        fecha_registro=now(),
                        paciente_id=paciente["id"],
                        personal_id=personal.id,
                        tipo_procedimiento_id=tipo_procedimiento.id,
                        id_procedimiento_especifico=procedimiento,
                    )
                    print(
                        f"✅ Registro añadido para medicamento '{medicamento.descripcion}'"
                    )

            messages.success(
                request, "✅ Procedimiento específico registrado con éxito."
            )
            print("Mensaje de éxito añadido")
            return redirect("r_procedimientos_especificos")

        except MaterialesInsumos.DoesNotExist as e:
            print(f"❌ Error: Material no encontrado. Detalles: {e}")
            messages.error(request, "Uno de los materiales no existe.")
        except Medicamentos.DoesNotExist as e:
            print(f"❌ Error: Medicamento no encontrado. Detalles: {e}")
            messages.error(request, "Uno de los medicamentos no existe.")
        except ValueError as e:
            print(f"❌ Error: {e}")
            messages.error(request, str(e))
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            messages.error(request, "Error inesperado al registrar el procedimiento.")

    # Contexto para renderizar el formulario
    context = {
        "title": "Registro de Procedimiento Específico",
        "persona": request.session.get("persona"),
        "tipo_procedimiento_id": request.session.get("tipo_procedimiento_id"),
    }
    return render(
        request, "op_topico/registros_procedimientos/proc_especificos.html", context
    )


@login_required
def r_procedimientos_especiales(request):
    if request.method == "POST":
        print("Datos recibidos en request.POST:", request.POST)

        # Obtener y procesar datos del formulario
        descripcion = request.POST.get("descripcion", "").strip()
        materiales = list(set(request.POST.getlist("materiales[]")))
        cantidades_materiales = request.POST.getlist("cantidades_materiales[]")
        procedimientos_especiales = request.POST.getlist("procedimientos_especiales[]")
        valores_adicionales = request.POST.getlist("valores_adicionales[]")

        # Validar datos recibidos
        if not procedimientos_especiales:
            print("⚠️ Error: No se recibieron procedimientos especiales.")
        else:
            print(
                f"✅ Procedimientos especiales seleccionados: {procedimientos_especiales}"
            )

        if not materiales:
            print("⚠️ Error: No se recibieron materiales.")
        else:
            print(f"✅ Materiales seleccionados: {materiales}")

        if not cantidades_materiales:
            print("⚠️ Error: No se recibieron cantidades de materiales.")
        else:
            print(f"✅ Cantidades de materiales: {cantidades_materiales}")

        # Recuperar datos de sesión
        paciente = request.session.get("persona")
        tipo_procedimiento_id = request.session.get("tipo_procedimiento_id")
        personal_id = request.session.get("personal_id")

        print(f"Paciente en sesión: {paciente}")
        print(f"Tipo de procedimiento en sesión: {tipo_procedimiento_id}")
        print(f"Personal logueado: {personal_id}")

        # Validar datos obligatorios de sesión
        if not paciente or not tipo_procedimiento_id or not personal_id:
            messages.error(
                request, "⚠️ Datos incompletos en la sesión. Por favor, verifica."
            )
            return redirect("r_procedimientos_especiales")

        try:
            # Recuperar instancias necesarias
            personal = User.objects.get(id=personal_id)
            tipo_procedimiento = TipoProcedimiento.objects.get(id=tipo_procedimiento_id)

            with transaction.atomic():
                # Registrar cada procedimiento especial
                for proc, valor in zip(procedimientos_especiales, valores_adicionales):
                    descripcion_proc = proc
                    valor_proc = valor if proc == "HGT" else None

                    procedimiento = RegistroProcedimientoEspeciales.objects.create(
                        fecha_registro=now(),
                        descripcion=descripcion_proc,
                        valor=valor_proc,
                        paciente_id=paciente["id"],
                        personal=personal,
                        tipo_procedimiento=tipo_procedimiento,
                    )
                    print(
                        f"✅ Procedimiento especial registrado: ID {procedimiento.id} - Descripción: {descripcion_proc}"
                    )

                # Procesar materiales asociados
                for material_id, cantidad in zip(materiales, cantidades_materiales):
                    cantidad = int(cantidad)
                    material = MaterialesInsumos.objects.get(id=material_id)

                    # Validar si hay stock suficiente
                    if material.stock_actual < cantidad:
                        raise ValueError(
                            f"Stock insuficiente para el material '{material.descripcion}'. Disponible: {material.stock_actual}, Requerido: {cantidad}."
                        )

                    # Registrar salida en RegistroMaterialesInsumos
                    RegistroMaterialesInsumos.objects.create(
                        materiales_insumos=material,
                        tipo_movimiento="salida",
                        cantidad=cantidad,
                        personal=personal,
                        paciente_id=paciente["id"],
                        tipo_procedimiento=tipo_procedimiento,
                        fecha_registro=now(),
                        id_procedimiento_especiales=procedimiento,
                    )
                    print(
                        f"✅ Salida registrada para material '{material.descripcion}' - Cantidad: {cantidad}"
                    )

                    # Reducir el stock del material
                    material.stock_actual -= cantidad
                    material.save()
                    print(
                        f"🔄 Stock actualizado para '{material.descripcion}': {material.stock_actual}"
                    )

            # Mostrar mensaje de éxito
            messages.success(request, "✅ Procedimiento especial registrado con éxito.")
            print("Mensaje de éxito añadido")
            return redirect("r_procedimientos_especiales")

        except MaterialesInsumos.DoesNotExist as e:
            print(f"❌ Error: Material no encontrado. Detalles: {e}")
            messages.error(request, "Uno de los materiales no existe.")
        except ValueError as e:
            print(f"❌ Error: {e}")
            messages.error(request, str(e))
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            messages.error(request, "Error inesperado al registrar el procedimiento.")

    # Contexto para renderizar el formulario
    context = {
        "title": "Registro de Procedimiento Especial",
        "persona": request.session.get("persona"),
        "tipo_procedimiento_id": request.session.get("tipo_procedimiento_id"),
    }
    return render(
        request, "op_topico/registros_procedimientos/proc_especiales.html", context
    )


@login_required
def r_procedimientos_curacion_heridas(request):
    if request.method == "POST":
        print("Datos recibidos en request.POST:", request.POST)

        # Obtener y procesar datos únicos
        curacion_tiempo = request.POST.getlist("curacion_tiempo[]")
        curacion_complejidad = request.POST.getlist("curacion_complejidad[]")
        curacion_fase = request.POST.getlist("curacion_fase[]")
        curacion_tipo = request.POST.getlist("curacion_tipo[]")
        diagnosticos = request.POST.getlist("diagnosticos[]")
        materiales = list(set(request.POST.getlist("materiales[]")))
        cantidades_materiales = request.POST.getlist("cantidades_materiales[]")

        # Validar datos recibidos
        if not (
            curacion_tiempo and curacion_complejidad and curacion_fase and curacion_tipo
        ):
            print("⚠️ Error: Faltan datos para curación de heridas.")
        else:
            print(f"✅ Datos de curación por tiempo: {curacion_tiempo}")
            print(f"✅ Datos de curación por complejidad: {curacion_complejidad}")
            print(f"✅ Datos de curación por fase: {curacion_fase}")
            print(f"✅ Tipos de curación: {curacion_tipo}")

        if not diagnosticos:
            print("⚠️ Error: No se recibieron diagnósticos médicos.")
        else:
            print(f"✅ Diagnósticos seleccionados: {diagnosticos}")

        if not materiales:
            print("⚠️ Error: No se recibieron materiales.")
        else:
            print(f"✅ Materiales seleccionados: {materiales}")

        if not cantidades_materiales:
            print("⚠️ Error: No se recibieron cantidades de materiales.")
        else:
            print(f"✅ Cantidades de materiales: {cantidades_materiales}")

        # Recuperar datos de sesión
        paciente = request.session.get("persona")
        tipo_procedimiento_id = request.session.get("tipo_procedimiento_id")
        personal_id = request.session.get("personal_id")

        print(f"Paciente en sesión: {paciente}")
        print(f"Tipo de procedimiento en sesión: {tipo_procedimiento_id}")
        print(f"Personal logueado: {personal_id}")

        # Validar datos obligatorios
        if not paciente or not tipo_procedimiento_id or not personal_id:
            messages.error(
                request, "⚠️ Datos incompletos en la sesión. Por favor, verifica."
            )
            return redirect("r_procedimientos_curacion_heridas")

        try:
            # Recuperar instancias necesarias
            personal = User.objects.get(id=personal_id)
            tipo_procedimiento = TipoProcedimiento.objects.get(id=tipo_procedimiento_id)

            with transaction.atomic():
                # Registrar curaciones de heridas
                for tiempo, complejidad, fase, tipo in zip(
                    curacion_tiempo, curacion_complejidad, curacion_fase, curacion_tipo
                ):
                    curacion = RegistroCuracionHerida.objects.create(
                        fecha_registro=now(),
                        xtiempo=tiempo,
                        xcomplejidad=complejidad,
                        fase=fase,
                        tipo_curacion=tipo,
                        paciente_id=paciente["id"],
                        personal=personal,
                        tipo_procedimiento=tipo_procedimiento,
                    )
                    print(f"✅ Curación de herida registrada: ID {curacion.id}")

                # Registrar diagnósticos médicos
                for diagnostico_id in diagnosticos:
                    diagnostico = DiagnosticoMedico.objects.get(id=diagnostico_id)
                    registro_diagnostico = RegistroDiagnosticoMedico.objects.create(
                        paciente_id=paciente["id"],
                        personal=personal,
                        diagnostico_medico=diagnostico,
                        fecha_registro=now(),
                        tipo_procedimiento=tipo_procedimiento,
                        id_procedimiento_curacion=curacion,
                    )
                    print(
                        f"✅ Diagnóstico médico registrado: ID {registro_diagnostico.id} - Descripción: {diagnostico.descripcion}"
                    )

                # Procesar materiales asociados
                for material_id, cantidad in zip(materiales, cantidades_materiales):
                    cantidad = int(cantidad)
                    material = MaterialesInsumos.objects.get(id=material_id)

                    # Validar stock suficiente
                    if material.stock_actual < cantidad:
                        raise ValueError(
                            f"Stock insuficiente para '{material.descripcion}'. Disponible: {material.stock_actual}, Requerido: {cantidad}."
                        )

                    # Registrar salida de material
                    RegistroMaterialesInsumos.objects.create(
                        materiales_insumos=material,
                        tipo_movimiento="salida",
                        cantidad=cantidad,
                        personal=personal,
                        paciente_id=paciente["id"],
                        tipo_procedimiento=tipo_procedimiento,
                        fecha_registro=now(),
                        id_procedimiento_curacion=curacion,
                    )
                    print(
                        f"✅ Salida registrada: {material.descripcion} - Cantidad: {cantidad}"
                    )

                    # Reducir stock del material
                    material.stock_actual -= cantidad
                    material.save()
                    print(
                        f"🔄 Stock actualizado para '{material.descripcion}': {material.stock_actual}"
                    )

            # Mensaje de éxito
            messages.success(request, "✅ Curación de heridas registrada con éxito.")
            print("Mensaje de éxito añadido")
            return redirect("r_procedimientos_curacion_heridas")

        except MaterialesInsumos.DoesNotExist:
            print("❌ Error: Uno de los materiales no existe.")
            messages.error(request, "Uno de los materiales no existe.")
        except ValueError as e:
            print(f"❌ Error: {e}")
            messages.error(request, str(e))
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            messages.error(
                request, "Error inesperado al registrar la curación de heridas."
            )

    # Contexto para renderizar el formulario
    diagnosticos = DiagnosticoMedico.objects.all()
    context = {
        "title": "Registro de Curación de Heridas",
        "persona": request.session.get("persona"),
        "tipo_procedimiento_id": request.session.get("tipo_procedimiento_id"),
        "diagnosticos": diagnosticos,
    }
    return render(
        request,
        "op_topico/registros_procedimientos/proc_curacion_heridas.html",
        context,
    )


@login_required
def r_procedimientos_medicos(request):
    if request.method == "POST":
        print("Datos recibidos en request.POST:", request.POST)

        # Obtener y procesar datos únicos
        descripcion = request.POST.get("descripcion", "").strip()
        materiales = list(set(request.POST.getlist("materiales[]")))
        cantidades_materiales = request.POST.getlist("cantidades_materiales[]")
        procedimientos_medicos = request.POST.getlist("procedimientos_medicos[]")
        descripciones_medicos = request.POST.getlist("descripciones_medicos[]")

        # Validar datos recibidos
        if not procedimientos_medicos:
            print("⚠️ Error: No se recibieron procedimientos médicos.")
        else:
            print(f"✅ Procedimientos médicos seleccionados: {procedimientos_medicos}")

        if not materiales:
            print("⚠️ Error: No se recibieron materiales.")
        else:
            print(f"✅ Materiales seleccionados: {materiales}")

        if not cantidades_materiales:
            print("⚠️ Error: No se recibieron cantidades de materiales.")
        else:
            print(f"✅ Cantidades de materiales: {cantidades_materiales}")

        # Recuperar datos de sesión
        paciente = request.session.get("persona")
        tipo_procedimiento_id = request.session.get("tipo_procedimiento_id")
        personal_id = request.session.get("personal_id")

        print(f"Paciente en sesión: {paciente}")
        print(f"Tipo de procedimiento en sesión: {tipo_procedimiento_id}")
        print(f"Personal logueado: {personal_id}")

        # Validar datos obligatorios
        if not paciente or not tipo_procedimiento_id or not personal_id:
            messages.error(
                request, "⚠️ Datos incompletos en la sesión. Por favor, verifica."
            )
            return redirect("r_procedimientos_medicos")

        try:
            # Recuperar instancias necesarias
            personal = User.objects.get(id=personal_id)
            tipo_procedimiento = TipoProcedimiento.objects.get(id=tipo_procedimiento_id)

            with transaction.atomic():
                # Registrar procedimientos médicos
                for proc, descripcion_proc in zip(
                    procedimientos_medicos, descripciones_medicos
                ):
                    procedimiento = RegistroProcedimientoMedicos.objects.create(
                        fecha_registro=now(),
                        descripcion=descripcion_proc,  # Asignar la descripción correspondiente
                        paciente_id=paciente["id"],
                        personal=personal,
                        tipo_procedimiento=tipo_procedimiento,
                    )
                    print(
                        f"✅ Procedimiento médico registrado: ID {procedimiento.id} - Descripción: {descripcion_proc}"
                    )

                # Procesar materiales asociados
                for material_id, cantidad in zip(materiales, cantidades_materiales):
                    cantidad = int(cantidad)
                    material = MaterialesInsumos.objects.get(id=material_id)

                    # Validar stock suficiente
                    if material.stock_actual < cantidad:
                        raise ValueError(
                            f"Stock insuficiente para '{material.descripcion}'. Disponible: {material.stock_actual}, Requerido: {cantidad}."
                        )

                    # Registrar salida en materiales
                    RegistroMaterialesInsumos.objects.create(
                        materiales_insumos=material,
                        tipo_movimiento="salida",
                        cantidad=cantidad,
                        personal=personal,
                        paciente_id=paciente["id"],
                        tipo_procedimiento=tipo_procedimiento,
                        fecha_registro=now(),
                        id_procedimiento_medico=procedimiento,
                    )
                    print(
                        f"✅ Salida registrada: {material.descripcion} - Cantidad: {cantidad}"
                    )

                    # Actualizar el stock del material
                    material.stock_actual -= cantidad
                    material.save()
                    print(
                        f"🔄 Stock actualizado para '{material.descripcion}': {material.stock_actual}"
                    )

            # Mensaje de éxito
            messages.success(request, "✅ Procedimiento médico registrado con éxito.")
            print("Mensaje de éxito añadido")
            return redirect("r_procedimientos_medicos")

        except MaterialesInsumos.DoesNotExist:
            print("❌ Error: Uno de los materiales no existe.")
            messages.error(request, "Uno de los materiales no existe.")
        except ValueError as e:
            print(f"❌ Error: {e}")
            messages.error(request, str(e))
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            messages.error(
                request, "Error inesperado al registrar el procedimiento médico."
            )

    # Contexto para renderizar el formulario
    context = {
        "title": "Registro de Procedimiento Médico",
        "persona": request.session.get("persona"),
        "tipo_procedimiento_id": request.session.get("tipo_procedimiento_id"),
    }
    return render(
        request, "op_topico/registros_procedimientos/proc_medicos.html", context
    )
