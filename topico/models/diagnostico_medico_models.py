from django.db import models
from .procedimientos_models import TipoProcedimiento
from .procedimientos_models import RegistroCuracionHerida
from .pacientes_models import Paciente
from django.contrib.auth.models import User


class DiagnosticoMedico(models.Model):
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion


class RegistroDiagnosticoMedico(models.Model):
    diagnostico_medico = models.ForeignKey(
        DiagnosticoMedico, on_delete=models.CASCADE, null=True, blank=True
    )
    tipo_procedimiento = models.ForeignKey(
        TipoProcedimiento, on_delete=models.CASCADE, null=True, blank=True
    )
    personal = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, null=True, blank=True
    )

    fecha_registro = models.DateField(
        auto_now_add=True, null=True, blank=True
    )  # Fecha automática de registro

    id_procedimiento_curacion = models.ForeignKey(
        RegistroCuracionHerida,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.diagnostico_medico} - {self.tipo_procedimiento}"

    def get_diagmedico_details(self):
        """Retorna los detalles relevantes del procedimiento general como un diccionario"""
        return {
            "Diagnostico_Medico": self.diagnostico_medico.descripcion,
        }
