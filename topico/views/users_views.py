from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import (
    MaterialesInsumos,
    RegistroMaterialesInsumos,
    TipoProcedimiento,
    RegistroProcedimientoEspecifico,
    RegistroProcedimientoEspeciales,
    RegistroCuracionHerida,
    RegistroDiagnosticoMedico,
    RegistroProcedimientoMedicos,
    Procedimiento,
)
from django.db.models import Count, Sum, F
from datetime import datetime, timedelta


def register_user(request):
    if request.method == "GET":
        return render(request, "register_user.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Creando el usuario
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("login_user")  # Cambia la vista a listado o index
            except Exception as e:
                return render(
                    request,
                    "register_user.html",
                    {"form": UserCreationForm, "error": f"hubo error: {str(e)}"},
                )
        return render(
            request,
            "register_user.html",
            {"form": UserCreationForm, "error": "contraseña no coincide"},
        )


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                request.session["personal_id"] = user.id
                return redirect("dashboard")
            else:
                messages.error(request, "Usuario o contraseña es incorrecta")
        else:
            messages.error(request, "Usuario o contraseña es incorrecta")
    else:
        form = AuthenticationForm
    return render(request, "auth/login.html", {"form": form})


@login_required
def logout_sesion(request):
    logout(request)
    return redirect("login_user")


@login_required
def dashboard(request):
    # 1. Stock actual de materiales e insumos
    stock_materiales = MaterialesInsumos.objects.annotate(
        porcentaje_uso=(F("stock_actual") * 100) / F("stock_minimo")
    ).values(
        "descripcion", "stock_actual", "unidad_medida", "stock_minimo", "porcentaje_uso"
    )

    # Filtrar materiales en alerta
    alertas_stock = MaterialesInsumos.objects.filter(
        estado="activo",
        stock_actual__lt=F(
            "stock_minimo"
        ),  # Filtrar donde el stock actual sea menor al mínimo
    ).values("descripcion", "stock_actual", "unidad_medida", "stock_minimo")

    # 2. Procedimientos realizados por tipo
    total_generales = Procedimiento.objects.filter(
        tipo_procedimiento__descripcion="General"
    ).count()
    total_especificos = RegistroProcedimientoEspecifico.objects.count()
    total_especiales = RegistroProcedimientoEspeciales.objects.count()
    total_curaciones = RegistroCuracionHerida.objects.count()
    total_medicos = RegistroProcedimientoMedicos.objects.count()

    procedimientos_realizados = {
        "Generales": total_generales,
        "Específicos": total_especificos,
        "Especiales": total_especiales,
        "Curaciones": total_curaciones,
        "Médicos": total_medicos,
    }

    # 3. Diagnósticos más comunes
    diagnosticos_comunes = (
        RegistroDiagnosticoMedico.objects.values("diagnostico_medico__descripcion")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    # 4. Materiales más usados
    materiales_usados = (
        RegistroMaterialesInsumos.objects.filter(materiales_insumos__estado="activo")
        .values("materiales_insumos__descripcion")
        .annotate(total_usado=Sum("cantidad"))
        .order_by("-total_usado")[:5]
    )

    # 5. Evolución de curaciones de heridas
    ultimos_30_dias = datetime.now() - timedelta(days=30)
    evolucion_curaciones = (
        RegistroCuracionHerida.objects.filter(fecha_registro__gte=ultimos_30_dias)
        .values("fecha_registro")
        .annotate(total=Count("id"))
        .order_by("fecha_registro")
    )

    # KPIs
    total_procedimientos = sum(procedimientos_realizados.values())
    total_diagnosticos = RegistroDiagnosticoMedico.objects.count()

    # Calcular la fecha del primer día del mes anterior
    hoy = datetime.now()
    primer_dia_mes_actual = datetime(hoy.year, hoy.month, 1)
    primer_dia_mes_anterior = primer_dia_mes_actual - timedelta(days=1)
    ultimo_dia_mes_anterior = primer_dia_mes_anterior
    primer_dia_mes_anterior = datetime(
        ultimo_dia_mes_anterior.year, ultimo_dia_mes_anterior.month, 1
    )

    # Consultar procedimientos del mes anterior
    procedimientos_mes_anterior = Procedimiento.objects.filter(
        fecha_registro__gte=primer_dia_mes_anterior,
        fecha_registro__lt=primer_dia_mes_actual,
    ).count()

    cambio_procedimientos = (
        ((total_procedimientos - procedimientos_mes_anterior) / total_procedimientos)
        * 100
        if total_procedimientos > 0
        else 0
    )

    # Calcular ocupación de insumos
    total_stock_minimo = (
        MaterialesInsumos.objects.aggregate(total_minimo=Sum("stock_minimo"))[
            "total_minimo"
        ]
        or 0
    )
    total_stock_actual = (
        MaterialesInsumos.objects.aggregate(total_actual=Sum("stock_actual"))[
            "total_actual"
        ]
        or 0
    )

    if total_stock_minimo > 0:
        ocupacion_insumos = (
            (total_stock_minimo - total_stock_actual) / total_stock_minimo
        ) * 100
        ocupacion_insumos = max(min(ocupacion_insumos, 100), 0)
    else:
        ocupacion_insumos = 0

    # Contexto para la plantilla
    context = {
        "stock_materiales": stock_materiales,
        "alertas_stock": alertas_stock,  # Materiales en alerta
        "procedimientos_realizados": procedimientos_realizados,
        "diagnosticos_comunes": diagnosticos_comunes,
        "materiales_usados": materiales_usados,
        "evolucion_curaciones": evolucion_curaciones,
        "total_procedimientos": total_procedimientos,
        "total_diagnosticos": total_diagnosticos,
        "cambio_procedimientos": round(cambio_procedimientos, 2),
        "ocupacion_insumos": round(ocupacion_insumos, 2),
        "title": "Dashboard",
    }

    return render(request, "dashboard.html", context)
