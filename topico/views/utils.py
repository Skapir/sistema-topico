from ..models import RegistroMaterialesInsumos


def calcular_saldo_acumulado(material):

    registros = RegistroMaterialesInsumos.objects.filter(
        materiales_insumos=material
    ).order_by("fecha_registro")

    saldo = material.stock_inicial
    registros_modificados = []

    # Agregar saldo inicial
    registros_modificados.append(
        {
            "fecha_registro": "Saldo Inicial",
            "tipo_procedimiento": "--",
            "entrada": "--",
            "salida": "--",
            "saldo": saldo,
        }
    )

    # Procesar los registros del material
    for registro in registros:
        if registro.tipo_movimiento == "entrada":
            saldo += registro.cantidad
        elif registro.tipo_movimiento == "salida":
            saldo -= registro.cantidad

        registros_modificados.append(
            {
                "fecha_registro": registro.fecha_registro,
                "tipo_procedimiento": (
                    registro.tipo_procedimiento.descripcion
                    if registro.tipo_procedimiento
                    else ""
                ),
                "entrada": (
                    registro.cantidad if registro.tipo_movimiento == "entrada" else "--"
                ),
                "salida": (
                    registro.cantidad if registro.tipo_movimiento == "salida" else "--"
                ),
                "saldo": saldo,
            }
        )

    return registros_modificados
