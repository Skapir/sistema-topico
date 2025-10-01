from django.db import models


class Paciente(models.Model):
    HI_NREG = models.IntegerField()
    HI_AUTASE = models.CharField(max_length=255)
    HI_NOMBRE = models.CharField(max_length=255)
    HI_FECNAC = models.DateField()
    HI_UBINAC = models.IntegerField()
    HI_DIRECC = models.CharField(max_length=255)
    HI_SEXO = models.CharField(max_length=255)
    HI_NDOCUM = models.IntegerField()
    HI_ESTCIV = models.CharField(max_length=255)
    HI_CPOLIC = models.CharField(max_length=255, default="valor_por_defecto")

    def __str__(self):
        return f"{self.HI_NREG} - {self.HI_NOMBRE} - {self.HI_FECNAC}"
