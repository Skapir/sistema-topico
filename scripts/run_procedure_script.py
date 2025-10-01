import os
import sys
import django

# Agrega la raíz del proyecto al PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configura el entorno Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "core.settings"
)  # Cambia 'core' al nombre del módulo que contiene tus settings.py
django.setup()

from topico.models import (
    RegistroProcedimientoEspecifico,
    Procedimiento,
    Medicamentos,
    MaterialesInsumos,
    RegistroMedicamentos,
    RegistroMaterialesInsumos,
)
from django.utils.timezone import now

# Crear un procedimiento específico
procedimiento_especifico = RegistroProcedimientoEspecifico.objects.create(
    tipo_procedimiento_id=2,  # ID de TipoProcedimiento (procedimiento general)
    personal_id=2,  # ID del usuario actual
    paciente_id=8,  # ID del paciente actual
    fecha_registro=now(),
    descripcion="Prueba Manual",
)
print(f"Procedimiento específico creado: {procedimiento_especifico}")

# Obtener el Procedimiento general asociado al tipo_procedimiento_id
procedimiento_general = Procedimiento.objects.get(
    id=procedimiento_especifico.tipo_procedimiento_id
)
print(f"Procedimiento general asociado: {procedimiento_general}")

# Crear medicamentos relacionados con el Procedimiento general
medicamento = Medicamentos.objects.get(id=2)  # Cambia el ID por uno válido
registro_medicamento = RegistroMedicamentos.objects.create(
    procedimiento=procedimiento_general,  # Procedimiento general
    medicamentos=medicamento,
    paciente_id=8,  # Mismo paciente
    personal_id=2,  # Mismo personal
    fecha_registro=now(),
)
print(f"Medicamento registrado: {registro_medicamento}")

# Crear materiales relacionados con el Procedimiento general
material = MaterialesInsumos.objects.get(id=78)  # Cambia el ID por uno válido
registro_material = RegistroMaterialesInsumos.objects.create(
    procedimiento=procedimiento_general,  # Procedimiento general
    materiales_insumos=material,
    cantidad=1,  # Cantidad de prueba
    paciente_id=8,  # Mismo paciente
    personal_id=2,  # Mismo personal
    fecha_registro=now(),
)
print(f"Material registrado: {registro_material}")
