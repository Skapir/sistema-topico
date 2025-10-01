from django.http import JsonResponse
from ..models import (
    Medicamentos,
)  # Asegúrate de importar tu modelo de medicamentos


def buscar_medicamentos(request):
    query = request.GET.get("q", "")
    medicamentos = Medicamentos.objects.filter(descripcion__icontains=query)[
        :10
    ]  # Filtra con un límite de 10
    resultados = [
        {
            "id": med.id,
            "descripcion": med.descripcion,
            "unidad_medida": med.unidad_medida,
        }
        for med in medicamentos
    ]
    return JsonResponse(resultados, safe=False)
