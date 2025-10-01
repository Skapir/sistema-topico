from django.db import models
from .personales_models import Personal
from .pacientes_models import Paciente
from django.contrib.auth.models import User
from datetime import timedelta


# Modelo de Tipo de Procedimiento
class TipoProcedimiento(models.Model):
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion


class Procedimiento(models.Model):
    fecha_registro = models.DateField(auto_now_add=True)
    observacion = models.CharField(max_length=255)
    tipo_procedimiento = models.ForeignKey(
        "TipoProcedimiento", on_delete=models.CASCADE
    )
    personal = models.ForeignKey(User, on_delete=models.CASCADE)
    paciente = models.ForeignKey("Paciente", on_delete=models.CASCADE)
    presion_arterial = models.CharField(max_length=20, blank=True, null=True)
    temperatura = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True
    )
    frecuencia_cardiaca = models.IntegerField(blank=True, null=True)
    saturacion_oxigeno = models.IntegerField(blank=True, null=True)
    volumen_oxigeno = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True
    )

    def __str__(self):
        return f"{self.tipo_procedimiento} - {self.fecha_registro}"

    def get_fecha(self):
        return self.fecha_registro

    def get_general_details(self):
        return {
            "Presión Arterial": self.presion_arterial,
            "Temperatura": self.temperatura,
            "Frecuencia Cardíaca": self.frecuencia_cardiaca,
            "Saturación Oxígeno": self.saturacion_oxigeno,
            "Volumen Oxígeno": self.volumen_oxigeno,
            "Observación": self.observacion,
        }


class RegistroProcedimientoEspecifico(models.Model):
    # datos FK
    tipo_procedimiento = models.ForeignKey(TipoProcedimiento, on_delete=models.CASCADE)
    personal = models.ForeignKey(User, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    # Datos de la misma tabla
    fecha_registro = models.DateField()
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tipo_procedimiento} - {self.fecha_registro}"

    def get_fecha(self):
        return self.fecha_registro

    def get_especifico_details(self):
        """Retorna los detalles relevantes del procedimiento general como un diccionario"""
        return {
            "descripcion_especifico": self.descripcion,
        }


class RegistroProcedimientoEspeciales(models.Model):
    # Relación con otras tablas (ForeignKey)
    tipo_procedimiento = models.ForeignKey(TipoProcedimiento, on_delete=models.CASCADE)
    personal = models.ForeignKey(User, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    # Datos del modelo
    fecha_registro = models.DateField(auto_now_add=True)  # Fecha automática de registro
    descripcion = models.CharField(
        max_length=255, blank=True, null=True
    )  # Descripción opcional
    valor = models.CharField(
        max_length=255, blank=True, null=True
    )  # Valor opcional (para HGT)

    def __str__(self):
        return f"{self.tipo_procedimiento} -{self.descripcion}- {self.fecha_registro} - {self.valor or 'N/A'}"

    def get_fecha(self):
        return self.fecha_registro

    def get_especial_details(self):
        """Retorna los detalles relevantes del procedimiento general como un diccionario"""
        return {"Descripcion": self.descripcion, "Valor": self.valor}


class RegistroProcedimientoMedicos(models.Model):
    # Relación con otras tablas (ForeignKey)
    tipo_procedimiento = models.ForeignKey(TipoProcedimiento, on_delete=models.CASCADE)
    personal = models.ForeignKey(User, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    # Datos del modelo
    fecha_registro = models.DateField(auto_now_add=True)  # Fecha automática de registro
    descripcion = models.CharField(
        max_length=255, blank=True, null=True
    )  # Descripción opcional

    def __str__(self):
        return f"{self.tipo_procedimiento} -{self.descripcion}- {self.fecha_registro}"

    def get_fecha(self):
        return self.fecha_registro

    def get_medico_details(self):
        """Retorna los detalles relevantes del procedimiento general como un diccionario"""
        return {
            "Descripcion": self.descripcion,
        }


class RegistroCuracionHerida(models.Model):
    # Relación con otras tablas (ForeignKey)
    tipo_procedimiento = models.ForeignKey(TipoProcedimiento, on_delete=models.CASCADE)
    personal = models.ForeignKey(User, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    # Datos del modelo
    fecha_registro = models.DateField(auto_now_add=True)  # Fecha automática de registro
    xtiempo = models.CharField(max_length=255, blank=True, null=True)
    xcomplejidad = models.CharField(max_length=255, blank=True, null=True)
    fase = models.CharField(max_length=255, blank=True, null=True)
    tipo_curacion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_procedimiento} -{self.xtiempo}- {self.fecha_registro}"

    def get_fecha(self):
        return self.fecha_registro

    def get_curacion_details(self):
        """Retorna los detalles relevantes del procedimiento general como un diccionario"""
        return {
            "X Tiempo": self.xtiempo,
            "X Complejidad": self.xcomplejidad,
            "Fase": self.fase,
            "Tipo Herida": self.tipo_curacion,
        }
