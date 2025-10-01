# models/__init__.py

from .procedimientos_models import (
    Procedimiento,
    TipoProcedimiento,
    RegistroProcedimientoEspecifico,
    RegistroProcedimientoEspeciales,
    RegistroProcedimientoMedicos,
    RegistroCuracionHerida,
)
from .pacientes_models import Paciente
from .personales_models import Personal, TipoPersonal
from .medicamentos_models import Medicamentos, RegistroMedicamentos
from .materiales_insumos_models import MaterialesInsumos, RegistroMaterialesInsumos
from .diagnostico_medico_models import DiagnosticoMedico, RegistroDiagnosticoMedico
