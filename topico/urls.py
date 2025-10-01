from django.urls import path
from .views import (
    users_views,
    pacientes_views,
    materiales_insumos_views,
    personales_views,
    procedimientos_views,
    medicamentos_views,
)


urlpatterns = [
    # Users
    path("", users_views.login_user, name="login_user"),
    path("register/", users_views.register_user, name="register"),
    path("logout/", users_views.logout_sesion, name="logout_sesion"),
    path("dashboard/", users_views.dashboard, name="dashboard"),
    # Pacientes
    path("optopico/", pacientes_views.optopico, name="optopico"),
    path("c_pacientes/", pacientes_views.c_pacientes, name="c_pacientes"),
    path("rp_pacientes/", pacientes_views.rp_pacientes, name="rp_pacientes"),
    path(
        "consultar_atenciones/",
        pacientes_views.consultar_atenciones_paciente,
        name="consultar_atenciones_paciente",
    ),
    path(
        "generar_pdf_atencion/<int:atencion_id>/<str:tipo_procedimiento>/",
        pacientes_views.generar_pdf_atencion,
        name="generar_pdf_atencion",
    ),
    # Personales
    path("c_personales/", personales_views.c_personales, name="c_personales"),
    # Materiales e Insumos
    path(
        "r_materiales_insumos/",
        materiales_insumos_views.r_materiales_insumos,
        name="r_materiales_insumos",
    ),
    path(
        "registrar_material/",
        materiales_insumos_views.registrar_material,
        name="registrar_material",
    ),
    path(
        "eliminar_material/<int:id>/",
        materiales_insumos_views.eliminar_material,
        name="eliminar_material",
    ),
    path(
        "actualizar_material/<int:id>/",
        materiales_insumos_views.actualizar_material,
        name="actualizar_material",
    ),
    path(
        "agregar-stock/<int:id>/",
        materiales_insumos_views.agregar_stock,
        name="agregar_stock",
    ),
    path(
        "rp_materiales/",
        materiales_insumos_views.rp_materiales_insumos,
        name="rp_materiales",
    ),
    path(
        "export_kardex_excel/",
        materiales_insumos_views.export_kardex_excel,
        name="export_kardex_excel",
    ),
    path(
        "export_kardex_pdf/",
        materiales_insumos_views.export_kardex_pdf,
        name="export_kardex_pdf",
    ),
    path(
        "optopico/buscar-materiales/",
        materiales_insumos_views.buscar_materiales,
        name="buscar_materiales",
    ),
    path(
        "optopico/buscar-materiales-insumos/",
        materiales_insumos_views.buscar_materiales_insumos,
        name="buscar_materiales_insumos",
    ),
    # Procedimientos
    path(
        "rp_procedimientos/",
        procedimientos_views.rp_procedimientos,
        name="rp_procedimientos",
    ),
    path(
        "export_procedimientos_excel/",
        procedimientos_views.export_procedimientos_excel,
        name="export_procedimientos_excel",
    ),
    path(
        "export_procedimientos_pdf/",
        procedimientos_views.export_procedimientos_pdf,
        name="export_procedimientos_pdf",
    ),
    path(
        "r_procedimientos/",
        procedimientos_views.r_procedimientos,
        name="r_procedimientos",
    ),
    path(
        "optopico/proc_generales/",
        procedimientos_views.r_procedimientos_generales,
        name="r_procedimientos_generales",
    ),
    path(
        "optopico/proc_especificos/",
        procedimientos_views.r_procedimientos_especificos,
        name="r_procedimientos_especificos",
    ),
    path(
        "optopico/proc_especiales/",
        procedimientos_views.r_procedimientos_especiales,
        name="r_procedimientos_especiales",
    ),
    path(
        "optopico/proc_curacion_heridas/",
        procedimientos_views.r_procedimientos_curacion_heridas,
        name="r_procedimientos_curacion_heridas",
    ),
    path(
        "optopico/proc_medicos/",
        procedimientos_views.r_procedimientos_medicos,
        name="r_procedimientos_medicos",
    ),
    # Medicamentos
    path(
        "optopico/buscar-medicamentos/",
        medicamentos_views.buscar_medicamentos,
        name="buscar_medicamentos",
    ),
]
