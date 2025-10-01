from django.db import models
from .procedimientos_models import (
    TipoProcedimiento,
    RegistroProcedimientoEspecifico,
    RegistroProcedimientoEspeciales,
    RegistroCuracionHerida,
    RegistroProcedimientoMedicos,
)
from .pacientes_models import Paciente
from django.contrib.auth.models import User


class MaterialesInsumos(models.Model):
    descripcion = models.CharField(max_length=255, null=False, blank=False)
    fecha_vencimiento = models.DateField(null=True, blank=False)
    stock_actual = models.PositiveIntegerField(default=0)
    stock_inicial = models.PositiveIntegerField(default=0)
    unidad_medida = models.CharField(max_length=255, null=False, blank=False)
    stock_minimo = models.PositiveIntegerField(default=0)
    fecha_registro = models.DateField(default="2024-11-26")
    estado = models.CharField(
        max_length=10,
        choices=[("activo", "Activo"), ("inactivo", "Inactivo")],
        default="activo",
    )

    def __str__(self):
        return f"{self.descripcion} - {self.stock_actual} {self.unidad_medida}"

    def is_below_minimum(self):
        """Comprueba si el stock actual está por debajo del mínimo."""
        return self.stock_actual < self.stock_minimo


class RegistroMaterialesInsumos(models.Model):
    MOVIMIENTO_CHOICES = [
        ("entrada", "Entrada"),
        ("salida", "Salida"),
    ]

    # Relaciones
    personal = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, null=True, blank=True
    )
    tipo_procedimiento = models.ForeignKey(
        TipoProcedimiento, on_delete=models.CASCADE, null=True, blank=True
    )
    materiales_insumos = models.ForeignKey(MaterialesInsumos, on_delete=models.CASCADE)

    # Campos adicionales
    cantidad = models.IntegerField()
    tipo_movimiento = models.CharField(
        max_length=10,
        choices=[("entrada", "Entrada"), ("salida", "Salida")],
        default="entrada",  # Valor predeterminado
    )
    fecha_registro = models.DateField(auto_now_add=True)
    id_procedimiento_especifico = models.ForeignKey(
        RegistroProcedimientoEspecifico,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="registromateriales_set",
    )
    id_procedimiento_especiales = models.ForeignKey(
        RegistroProcedimientoEspeciales,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    id_procedimiento_curacion = models.ForeignKey(
        RegistroCuracionHerida,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    id_procedimiento_medico = models.ForeignKey(
        RegistroProcedimientoMedicos,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.personal} - {self.materiales_insumos} - {self.tipo_movimiento} - {self.cantidad} - {self.fecha_registro}"

    def get_materiales_details(self):
        """Retorna los detalles relevantes del procedimiento general como un diccionario"""
        return {
            "Material": self.materiales_insumos.descripcion,
            "Cantidad": self.cantidad,
        }
