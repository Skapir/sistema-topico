from django.contrib import admin
from .models.diagnostico_medico_models import *
from .models.materiales_insumos_models import *
from .models.medicamentos_models import *
from .models.pacientes_models import *
from .models.personales_models import *
from .models.procedimientos_models import *


# Registra modelo DIAGNOSTICO MEDICOS
admin.site.register(DiagnosticoMedico)
admin.site.register(RegistroDiagnosticoMedico)
# Registra modelo MATERIALES E INSUMOS
admin.site.register(MaterialesInsumos)
admin.site.register(RegistroMaterialesInsumos)
# Registra modelo MEDICAMENTOS
admin.site.register(Medicamentos)
admin.site.register(RegistroMedicamentos)
# Registra modelo PACIENTES
admin.site.register(Paciente)
# Registra modelo PERSONALES
admin.site.register(TipoPersonal)
admin.site.register(Personal)
# Registra modelo PROCEDIMIENTOS
admin.site.register(TipoProcedimiento)
admin.site.register(Procedimiento)
admin.site.register(RegistroProcedimientoEspecifico)
admin.site.register(RegistroProcedimientoEspeciales)
admin.site.register(RegistroProcedimientoMedicos)
admin.site.register(RegistroCuracionHerida)
