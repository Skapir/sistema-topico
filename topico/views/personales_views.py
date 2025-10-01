from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def c_personales(request):
    # Contexto para enviar a la plantilla
    context = {
        "title": "Consulta de Personales",
        "user": request.user,
    }
    return render(request, "op_consultas/c_personales.html", context)
