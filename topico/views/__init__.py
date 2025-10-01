from .users_views import register_user, login_user, logout_sesion, dashboard
from .materiales_insumos_views import (
    r_materiales_insumos,
    rp_materiales_insumos,
    registrar_material,
    agregar_stock,
)
from .pacientes_views import optopico, c_pacientes, rp_pacientes
from .personales_views import c_personales
from .procedimientos_views import (
    r_procedimientos,
    rp_procedimientos,
    r_procedimientos_especificos,
    r_procedimientos_especiales,
    r_procedimientos_generales,
    r_procedimientos_medicos,
)

__all__ = [
    "register_user",
    "login_user",
    "logout_sesion",
    "dashboard",
    "optopico",
    "c_pacientes",
    "rp_pacientes",
    "registrar_material",
    "r_materiales_insumos",
    "rp_materiales_insumos",
    "rp_materiales",
    "agregar_stock",
    "c_personales",
    "r_procedimientos",
    "rp_procedimientos",
    "r_procedimientos_especificos",
    "r_procedimientos_especiales",
    "r_procedimientos_generales",
    "r_procedimientos_medicos",
]
