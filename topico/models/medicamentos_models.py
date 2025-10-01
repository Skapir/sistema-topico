from django.db import models
from .procedimientos_models import TipoProcedimiento, RegistroProcedimientoEspecifico
from .pacientes_models import Paciente
from django.contrib.auth.models import User


class Medicamentos(models.Model):
    descripcion = models.CharField(max_length=255)
    unidad_medida = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.descripcion} - {self.unidad_medida}"


class RegistroMedicamentos(models.Model):
    # datos FK
    personal = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, null=True, blank=True
    )
    medicamentos = models.ForeignKey(Medicamentos, on_delete=models.CASCADE)
    tipo_procedimiento = models.ForeignKey(
        TipoProcedimiento,
        on_delete=models.CASCADE,
        null=True,  # Permite valores nulos temporalmente
        blank=True,
    )
    id_procedimiento_especifico = models.ForeignKey(
        RegistroProcedimientoEspecifico, on_delete=models.CASCADE, null=True, blank=True
    )

    # Datos de la misma tabla
    fecha_registro = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.medicamentos}"

    def get_medicamento_details(self):
        """Retorna los detalles relevantes del procedimiento general como un diccionario"""
        return {
            "Medicamentos": self.medicamentos,
            "Unidad_Medida": self.medicamentos.unidad_medida,
        }
