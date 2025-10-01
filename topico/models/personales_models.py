from django.db import models


class TipoPersonal(models.Model):
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion


class Personal(models.Model):
    apellidos = models.CharField(max_length=255)
    nombres = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(max_length=8, unique=True, null=True, blank=True)
    tipo_personal = models.ForeignKey(
        TipoPersonal, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        tipo = self.tipo_personal.descripcion if self.tipo_personal else "Sin tipo"
        return f"{self.nombres} - {self.apellidos}- {self.dni} - {tipo}"
