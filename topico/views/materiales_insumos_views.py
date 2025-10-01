from datetime import datetime, date
from django.contrib import messages
from django.db import transaction
from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import MaterialesInsumos, RegistroMaterialesInsumos
import pandas as pd
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from ..views.utils import calcular_saldo_acumulado


@login_required
def registrar_material(request):
    if request.method == "POST":
        print("Datos recibidos en request.POST:", request.POST)

        # Obtener los datos del formulario
        descripcion = request.POST.get("descripcion", "").strip()
        fecha_vencimiento = request.POST.get("fecha_vencimiento", "").strip()
        unidad_medida = request.POST.get("unidad_medida", "").strip()
        stock_inicial = int(request.POST.get("stock_inicial", "0").strip())
        stock_minimo = int(request.POST.get("stock_minimo", "0").strip())

        # Validar campos obligatorios
        if not descripcion or not unidad_medida:
            messages.error(request, "⚠️ Los campos obligatorios no están completos.")
            return redirect("r_materiales_insumos")

        try:
            with transaction.atomic():
                # Crear el nuevo material
                nuevo_material = MaterialesInsumos.objects.create(
                    descripcion=descripcion,
                    fecha_vencimiento=fecha_vencimiento if fecha_vencimiento else None,
                    unidad_medida=unidad_medida,
                    stock_inicial=stock_inicial,
                    stock_actual=stock_inicial,
                    stock_minimo=stock_minimo,
                    fecha_registro=now(),
                )
                print(
                    f"✅ Nuevo material registrado: {nuevo_material.descripcion} (ID {nuevo_material.id})"
                )

            # Mensaje de éxito
            messages.success(request, "✅ Material registrado exitosamente.")
            return redirect("r_materiales_insumos")

        except Exception as e:
            print(f"❌ Error al registrar el material: {e}")
            messages.error(request, "Error inesperado al registrar el material.")
            return redirect("r_materiales_insumos")

    # Si no es un POST, redirigir al listado de materiales
    return redirect("r_materiales_insumos")


@login_required
def agregar_stock(request, id):
    # Obtener el material o devolver un error 404 si no existe
    material = get_object_or_404(MaterialesInsumos, id=id)

    if request.method == "POST":
        try:
            # Obtener datos del formulario
            cantidad = request.POST.get("cantidad", "").strip()

            # Validar que la cantidad no esté vacía
            if not cantidad:
                messages.error(request, "⚠️ La cantidad es obligatoria.")
                return redirect("r_materiales_insumos")

            # Validar que la cantidad sea un número válido y mayor a 0
            if not cantidad.isdigit() or int(cantidad) <= 0:
                messages.error(request, "⚠️ La cantidad debe ser un número mayor a 0.")
                return redirect("r_materiales_insumos")

            # Actualizar el stock del material
            cantidad = int(cantidad)
            material.stock_actual += cantidad
            material.save()

            # Registrar el movimiento como "Entrada" en la tabla de registros
            RegistroMaterialesInsumos.objects.create(
                personal=request.user,
                materiales_insumos=material,
                cantidad=cantidad,
                tipo_movimiento="entrada",
                fecha_registro=date.today(),
            )

            # Mostrar un mensaje de éxito
            messages.success(
                request,
                f"✅ {cantidad} unidades agregadas exitosamente al stock de {material.descripcion}.",
            )
            return redirect("r_materiales_insumos")
        except Exception as e:
            # Capturar cualquier error y mostrarlo en la consola y en la interfaz
            messages.error(request, f"❌ Error al agregar stock: {str(e)}")
            return redirect("r_materiales_insumos")

    # Contexto adicional si es necesario
    context = {"title": "Agregar Stock", "material": material}
    return render(
        request, "op_topico/materiales_insumos/r_materiales_insumos.html", context
    )


@login_required
def buscar_materiales_insumos(request):
    """
    Vista para buscar materiales específicos para r_materiales_insumos.
    """
    query = request.GET.get("q", "")
    page = int(request.GET.get("page", 1))

    materiales = MaterialesInsumos.objects.filter(
        estado="activo", descripcion__icontains=query
    ).order_by("id")
    paginator = Paginator(materiales, 20)  # 20 materiales por página

    materiales_pagina = paginator.get_page(page)

    data = {
        "materiales": [
            {
                "id": material.id,
                "descripcion": material.descripcion,
                "unidad_medida": material.unidad_medida,
                "fecha_vencimiento": material.fecha_vencimiento,
                "stock_actual": material.stock_actual,
                "stock_minimo": material.stock_minimo,
            }
            for material in materiales_pagina
        ],
        "paginacion": {
            "current_page": page,
            "total_pages": paginator.num_pages,
            "has_previous": materiales_pagina.has_previous(),
            "has_next": materiales_pagina.has_next(),
            "previous_page": (
                materiales_pagina.previous_page_number()
                if materiales_pagina.has_previous()
                else None
            ),
            "next_page": (
                materiales_pagina.next_page_number()
                if materiales_pagina.has_next()
                else None
            ),
        },
    }

    return JsonResponse(data)


@login_required
def eliminar_material(request, id):
    # Obtener el material o devolver 404 si no existe
    material = get_object_or_404(MaterialesInsumos, id=id)

    if request.method == "POST":
        try:
            # Cambiar el estado a inactivo
            material.estado = "inactivo"
            material.save()

            # Mensaje de éxito
            messages.success(
                request,
                f"✅ El material '{material.descripcion}' fue Elminado exitosamente.",
            )
            return redirect("r_materiales_insumos")
        except Exception as e:
            # Capturar y manejar errores
            messages.error(request, f"❌ Error al desactivar el material: {str(e)}")
            return redirect("r_materiales_insumos")

    # Si no es POST, redirigir al listado
    return redirect("r_materiales_insumos")


@login_required
def actualizar_material(request, id):
    material = get_object_or_404(MaterialesInsumos, id=id)

    if request.method == "POST":
        try:
            # Obtener datos del formulario
            descripcion = request.POST.get("descripcion_editar", "").strip()
            unidad_medida = request.POST.get("unidad_medida_editar", "").strip()
            fecha_vencimiento = request.POST.get("fecha_vencimiento_editar", "").strip()
            # stock_actual = request.POST.get("stock_actual_editar", "").strip()
            stock_minimo = request.POST.get("stock_minimo_editar", "").strip()

            # Validar campos obligatorios
            if not descripcion:
                messages.error(request, "⚠️ El campo Descripción es obligatorio.")
                return redirect("actualizar_material", id=material.id)

            if not unidad_medida:
                messages.error(request, "⚠️ El campo Unidad de Medida es obligatorio.")
                return redirect("actualizar_material", id=material.id)

            # if not stock_actual.isdigit() or int(stock_actual) < 0:
            # messages.error(
            # request, "⚠️ El Stock Actual debe ser un número mayor o igual a 0."
            # )
            # return redirect("actualizar_material", id=material.id)

            if not stock_minimo.isdigit() or int(stock_minimo) < 0:
                messages.error(
                    request, "⚠️ El Stock Mínimo debe ser un número mayor o igual a 0."
                )
                return redirect("actualizar_material", id=material.id)

            try:
                fecha_vencimiento = datetime.strptime(
                    fecha_vencimiento, "%Y-%m-%d"
                ).date()
            except ValueError:
                messages.error(request, "⚠️ La Fecha de Vencimiento no es válida.")
                return redirect("actualizar_material", id=material.id)

            # Actualizar el material
            material.descripcion = descripcion
            material.unidad_medida = unidad_medida
            material.fecha_vencimiento = fecha_vencimiento
            # material.stock_actual = int(stock_actual)
            material.stock_minimo = int(stock_minimo)
            material.save()

            messages.success(request, "✅ Material actualizado exitosamente.")
            return redirect("r_materiales_insumos")
        except Exception as e:
            messages.error(request, f"❌ Error al actualizar el material: {str(e)}")
            return redirect("actualizar_material", id=material.id)

    context = {"title": "Actualizar Material", "material": material}
    return render(
        request, "op_topico/materiales_insumos/r_materiales_insumos.html", context
    )


def buscar_materiales(request):
    query = request.GET.get("q", "")
    limite = int(request.GET.get("limite", 10))  # Límite por defecto es 10
    materiales = MaterialesInsumos.objects.filter(
        estado="activo", descripcion__icontains=query
    )[:limite]
    data = [
        {
            "id": mat.id,
            "descripcion": mat.descripcion,
            "fecha_vencimiento": mat.fecha_vencimiento,
            "unidad_medida": mat.unidad_medida,
        }
        for mat in materiales
    ]
    return JsonResponse(data, safe=False)


@login_required
def rp_materiales_insumos(request):
    material_id = request.GET.get("material_id")
    material_seleccionado = None
    registros = None

    if material_id:
        material_seleccionado = get_object_or_404(MaterialesInsumos, id=material_id)

        # Calcular el kardex usando utils
        registros = calcular_saldo_acumulado(material_seleccionado)

    context = {
        "title": "Reporte de Materiales e Insumos",
        "user": request.user,
        "materiales": MaterialesInsumos.objects.all()
        .filter(estado="activo")
        .order_by("descripcion")
        .filter(estado="activo"),
        "material_seleccionado": material_seleccionado,
        "registros": registros,
    }
    return render(request, "op_reportes/rp_materiales.html", context)


@login_required
def export_kardex_excel(request):
    material_id = request.GET.get("material_id")
    material = get_object_or_404(MaterialesInsumos, id=material_id)

    # Calcular el kardex usando utils
    registros_modificados = calcular_saldo_acumulado(material)

    # Crear un DataFrame para exportar
    df = pd.DataFrame(registros_modificados)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f'attachment; filename="kardex_{material.descripcion}.xlsx"'
    )

    with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Kardex")

    return response


@login_required
def export_kardex_pdf(request):
    material_id = request.GET.get("material_id")
    material = get_object_or_404(MaterialesInsumos, id=material_id)

    # Calcular el kardex usando utils
    registros_modificados = calcular_saldo_acumulado(material)

    # Renderizar el contenido HTML
    context = {
        "material": material,
        "registros": registros_modificados,
    }
    html_string = render_to_string("op_reportes/kardex_pdf.html", context)

    # Generar el PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="kardex_{material.descripcion}.pdf"'
    )

    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response


@login_required
def r_materiales_insumos(request):
    """
    Vista principal para gestionar materiales e insumos.
    """
    if request.method == "POST":
        descripcion = request.POST.get("descripcion")
        unidad_medida = request.POST.get("unidad_medida")
        stock_actual = request.POST.get("stock_actual")

        MaterialesInsumos.objects.create(
            descripcion=descripcion,
            unidad_medida=unidad_medida,
            stock_actual=stock_actual,
        )
        return redirect("r_materiales_insumos")
    context = {
        "title": "Listado Materiales",
        "user": request.user,
    }
    return render(
        request, "op_topico/materiales_insumos/r_materiales_insumos.html", context
    )
