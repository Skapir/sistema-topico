// ----ALERTA DE REGISTRO EXITOSO-----//
document.addEventListener("DOMContentLoaded", function () {
    const alertBox = document.querySelector(".alert");
    if (alertBox) {
        // Desaparece la alerta después de 5 segundos
        setTimeout(() => {
            alertBox.style.transition = "opacity 0.5s ease";
            alertBox.style.opacity = "0";
            setTimeout(() => {
                alertBox.remove(); // Elimina el elemento después de que se desvanezca
            }, 500); // Espera hasta que la transición termine
        }, 5000); // 5000 ms = 5 segundos
    }
});

// -------- MANEJO GENERAL DE MODALES -------- //

/**
 * Muestra un modal específico basado en su ID.
 * @param {string} idModal - El ID del modal que se desea mostrar.
 */
function mostrarModal(idModal) {
    const modal = document.getElementById(`modal-${idModal}`);
    if (modal) {
        modal.style.display = "flex"; // Mostrar el modal
    } else {
        console.error(`No se encontró el modal con ID modal-${idModal}`);
    }
}

/**
 * Cierra el modal de alerta.
 */
function cerrarModal() {
    const modales = document.querySelectorAll('[id^="modal-"]');
    modales.forEach((modal) => (modal.style.display = "none"));
}

/**
 * Asegura que al cargar la página, todos los modales estén ocultos.
 */
document.addEventListener("DOMContentLoaded", function () {
    const modales = document.querySelectorAll('[id^="modal-"]');
    modales.forEach((modal) => modal.classList.add("hidden"));

    // Mostrar modal de éxito si hay mensajes en el sistema
    const modalExito = document.getElementById("modal-exito");
    const showModalExito = document.body.dataset.showModalExito === "true";
    if (modalExito && showModalExito) {

        modalExito.classList.remove("hidden");
        modalExito.classList.add("flex");
    }
});

/**
 * Cierra el modal de éxito.
 */
function cerrarModalExito() {
    const modal = document.getElementById("modal-exito");
    if (modal) {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
    }
}

// -------- VALIDACIÓN Y REDIRECCIÓN DE PROCEDIMIENTOS -------- //

/**
 * Valida la selección de un procedimiento y gestiona la redirección.
 * @param {Event} event - El evento del formulario.
 */
function validarSeleccion(event) {
    const select = document.getElementById("tipo_procedimiento");
    const selectedValue = select.value;

    if (!selectedValue) {
        event.preventDefault(); // Evita la navegación si no se ha seleccionado nada
        mostrarModal("alerta"); // Muestra el modal de alerta si no hay selección
    } else {
        guardarTipoProcedimientoEnSesion(selectedValue, function () {
            redireccionarProcedimiento(selectedValue);
        });
    }
}

/**
 * Guarda el tipo de procedimiento seleccionado en la sesión.
 * @param {string} tipoProcedimientoId - El ID del tipo de procedimiento.
 * @param {Function} callback - Función a ejecutar después de guardar.
 */
function guardarTipoProcedimientoEnSesion(tipoProcedimientoId, callback) {
    fetch('/optopico/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Incluye el token CSRF
        },
        body: JSON.stringify({ tipo_procedimiento_id: tipoProcedimientoId })
    })
        .then(response => {
            if (response.ok) {
                callback(); // Llama a la redirección después de guardar
            } else {
                console.error("Error al guardar el tipo de procedimiento en la sesión");
            }
        });
}

/**
 * Obtiene el valor de una cookie específica.
 * @param {string} name - El nombre de la cookie.
 * @returns {string} El valor de la cookie.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Redirige al usuario según el tipo de procedimiento seleccionado.
 * @param {string} selectedValue - El valor seleccionado en el menú desplegable.
 */
function redireccionarProcedimiento(selectedValue) {
    const rutas = {
        "1": "proc_generales/",
        "2": "proc_especificos/",
        "3": "proc_especiales/",
        "4": "proc_curacion_heridas/",
        "5": "proc_medicos/"
    };

    if (rutas[selectedValue]) {
        window.location.href = rutas[selectedValue];
    } else {
        mostrarModal("alerta");
    }
}

// -------- GESTIÓN DE PROCEDIMIENTOS ESPECÍFICOS -------- //

/**
 * Maneja la selección y adición de procedimientos específicos a la tabla.
 */
document.addEventListener("DOMContentLoaded", function () {
    const formProcedimiento = document.getElementById("form-tipo-procedimiento");
    if (formProcedimiento) {
        formProcedimiento.addEventListener("submit", function (event) {
            event.preventDefault();

            const tipoSeleccionado = document.getElementById("tipo-procedimiento").value;
            const nombreCompleto = tipoSeleccionado; // Sin mapeo adicional
            const descripcionInput = document.getElementById("descripcion-procedimiento");
            descripcionInput.value = nombreCompleto;

            agregarFilaATablaProcedimiento(tipoSeleccionado, nombreCompleto);
            cerrarModal("tipo-procedimiento");
        });
    }
});

/**
 * Agrega una nueva fila a la tabla de procedimientos.
 * @param {string} tipo - El tipo de procedimiento.
 * @param {string} descripcion - La descripción del procedimiento.
 */
function agregarFilaATablaProcedimiento(tipo, descripcion) {
    const tabla = document.getElementById("tabla-tipo-procedimiento").querySelector("tbody");

    if (!tabla) {
        console.error("La tabla no se encontró o no tiene un cuerpo <tbody>.");
        return;
    }

    const filas = tabla.getElementsByTagName("tr").length;
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
        <td class="py-2 px-4 border-r text-center">${filas + 1}</td>
        <td class="py-2 px-4 border-r text-center">${descripcion}</td>
        <td class="py-2 px-4 text-center">
            <button class="bg-red-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-red-500"
                onclick="eliminarFilaProcedimiento(this)">Eliminar</button>
        </td>
    `;

    tabla.appendChild(nuevaFila);

    const formulario = document.querySelector("form");
    formulario.innerHTML += `
        <input type="hidden" name="procedimientos[]" value="${tipo}">
        <input type="hidden" name="descripciones[]" value="${descripcion}">
    `;
}

/**
 * Elimina una fila específica de la tabla de procedimientos.
 * @param {HTMLButtonElement} button - El botón que se hizo clic para eliminar la fila.
 */
function eliminarFilaProcedimiento(button) {
    const fila = button.parentElement.parentElement;
    fila.remove();
}

// -------- GESTIÓN DE MEDICAMENTOS -------- //

/**
 * Busca medicamentos en tiempo real según el texto ingresado.
 */
function buscarMedicamentos() {
    const query = document.getElementById("busqueda-medicamento").value.trim();

    if (query === "") {
        document.getElementById("tabla-resultados-medicamentos").innerHTML = "";
        return;
    }

    fetch(`/optopico/buscar-medicamentos/?q=${query}`)
        .then(response => response.json())
        .then(datos => {
            const tablaResultados = document.getElementById("tabla-resultados-medicamentos");
            tablaResultados.innerHTML = "";

            if (datos.length === 0) {
                const filaVacia = document.createElement("tr");
                filaVacia.innerHTML = `
                    <td colspan="4" class="py-2 px-4 text-center text-gray-500">No se encontraron medicamentos</td>
                `;
                tablaResultados.appendChild(filaVacia);
                return;
            }

            datos.forEach(medicamento => {
                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td class="py-2 px-4 border-r text-center">${medicamento.id}</td>
                    <td class="py-2 px-4 border-r">${medicamento.descripcion}</td>
                    <td class="py-2 px-4 border-r text-center">${medicamento.unidad_medida}</td>
                    <td class="py-2 px-4 text-center">
                        <button class="bg-blue-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-500"
                            onclick="seleccionarMedicamento(${medicamento.id}, '${medicamento.descripcion}', '${medicamento.unidad_medida}')">
                            Seleccionar
                        </button>
                    </td>
                `;
                tablaResultados.appendChild(fila);
            });
        })
        .catch(error => console.error("Error:", error));
}

/**
 * Selecciona un medicamento y lo agrega a la tabla.
 */
function seleccionarMedicamento(id, descripcion, unidad) {
    const tabla = document.getElementById("tabla-medicamento").querySelector("tbody");

    if (document.querySelector(`.input-medicamento-${id}`)) {
        alert("El medicamento ya ha sido seleccionado.");
        return;
    }

    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
        <td class="py-2 px-4 border-r text-center">${id}</td>
        <td class="py-2 px-4 border-r">${descripcion}</td>
        <td class="py-2 px-4 border-r text-center">${unidad}</td>
        <td class="py-2 px-4 text-center">
            <button class="bg-red-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-red-500"
                onclick="eliminarMedicamento(this, ${id})">Eliminar</button>
        </td>
    `;
    tabla.appendChild(nuevaFila);

    const contenedorInputs = document.getElementById("contenedor-inputs-medicamentos");
    contenedorInputs.innerHTML += `<input type="hidden" name="medicamentos[]" value="${id}" class="input-medicamento-${id}">`;

    cerrarModal();
}

/**
 * Elimina un medicamento de la tabla.
 */
function eliminarMedicamento(button, id) {
    button.parentElement.parentElement.remove();
    const input = document.querySelector(`.input-medicamento-${id}`);
    if (input) input.remove();
}

// -------- GESTIÓN DE MATERIALES -------- //

/**
 * Busca materiales en tiempo real según el texto ingresado.
 */
function buscarMaterialesTabla(pagina = 1) {
    const inputBusqueda = document.getElementById("busqueda-material-total");
    if (!inputBusqueda) {
        console.error("No se encontró el campo de búsqueda 'busqueda-material-total'.");
        return; // Detener la ejecución si el elemento no está presente
    }

    const query = inputBusqueda.value.trim();
    fetch(`/optopico/buscar-materiales-insumos/?q=${query}&page=${pagina}`)
        .then(response => {
            if (!response.ok) throw new Error("Error al obtener los datos del servidor.");
            return response.json();
        })
        .then(datos => {
            const tablaResultados = document.getElementById("tabla-resultados-materiales-total");
            if (!tablaResultados) {
                console.error("No se encontró la tabla 'tabla-resultados-materiales-total'.");
                return;
            }
            tablaResultados.innerHTML = "";

            if (!datos.materiales || datos.materiales.length === 0) {
                tablaResultados.innerHTML = `
                    <tr>
                        <td colspan="5" class="py-2 px-4 text-center text-gray-500">No se encontraron materiales.</td>
                    </tr>
                `;
                return;
            }

            datos.materiales.forEach(material => {
                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td class="border px-4 py-2 text-center">${material.id}</td>
                    <td class="border px-4 py-2">${material.descripcion}</td>
                    <td class="border px-4 py-2 text-center">${material.unidad_medida}</td>
                    <td class="border px-4 py-2 text-center">${material.fecha_vencimiento}</td>
                    <td class="border px-4 py-2 text-center">${material.stock_actual}</td>
                    <td class="border px-4 py-2 text-center">
                        <button 
                            type="button" 
                            class="bg-green-700 text-white px-6 py-2 rounded-md shadow-md hover:bg-green-500 transition-colors duration-300"
                            onclick="abrirModalActualizarMaterial(${material.id}, '${material.descripcion.replace(/'/g, "\\'")}','${material.unidad_medida.replace(/'/g, "\\'")}', '${material.fecha_vencimiento}','${material.stock_minimo}')">
                            Editar
                        </button>
                        <button 
                            type="button" 
                            class="bg-blue-600 text-white px-6 py-2 rounded-md shadow-md hover:bg-blue-500 transition-colors duration-300"
                            onclick="abrirModalAgregarStock(${material.id}, '${material.descripcion.replace(/'/g, "\\'")}')">
                            Agregar
                        </button>
                        <button 
                            type="button" 
                            class="bg-red-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-red-500"
                            onclick="abrirModalEliminarMaterial(${material.id}, '${material.descripcion.replace(/'/g, "\\'")}')">
                            Eliminar
                        </button>
                    </td>
                `;
                tablaResultados.appendChild(fila);
            });


            actualizarPaginacion(datos.paginacion);
        })
        .catch(error => console.error("Error al buscar materiales:", error));
}

// Función para cargar materiales en la tabla
function cargarMaterialesTabla(pagina = 1) {
    buscarMaterialesTabla(pagina);
}


// Función para actualizar la paginación
function actualizarPaginacion(paginacion) {
    const paginacionContainer = document.getElementById("paginacion-container");
    if (!paginacionContainer || !paginacion) return;

    let html = "";

    if (paginacion.has_previous) {
        html += `<a href="#" data-page="${paginacion.previous_page}" class="paginacion-link px-4 py-2 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300">Anterior</a>`;
    }

    for (let i = 1; i <= paginacion.total_pages; i++) {
        html += `<a href="#" data-page="${i}" class="paginacion-link px-4 py-2 rounded-lg ${i === paginacion.current_page ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-700 hover:bg-gray-300"}">${i}</a>`;
    }

    if (paginacion.has_next) {
        html += `<a href="#" data-page="${paginacion.next_page}" class="paginacion-link px-4 py-2 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300">Siguiente</a>`;
    }

    paginacionContainer.innerHTML = html;

    paginacionContainer.querySelectorAll(".paginacion-link").forEach(enlace => {
        enlace.addEventListener("click", function (event) {
            event.preventDefault();
            const pagina = parseInt(this.getAttribute("data-page"));
            buscarMaterialesTabla(pagina);
        });
    });
}

// Escuchar eventos del campo de búsqueda y cargar datos iniciales
document.addEventListener("DOMContentLoaded", () => {
    const busquedaInput = document.getElementById("busqueda-material-total");
    const tablaResultados = document.getElementById("tabla-resultados-materiales-total");

    if (busquedaInput && tablaResultados) {
        busquedaInput.addEventListener("input", () => buscarMaterialesTabla(1));
        cargarMaterialesTabla(1);
    } else {
        //console.warn("Elementos relacionados con materiales no se encontraron en esta vista.");
        return;
    }
});

//----- OBTENER DATOS DE LA TABLA PARA EDITAR MATERIAL-----//
function abrirModalActualizarMaterial(materialId, descripcion, unidadMedida, fechaVencimiento, stockMinimo) {
    const modal = document.getElementById('modal-actualizar-material');
    if (!modal) {
        console.error("No se encontró el modal con ID 'modal-actualizar-material'.");
        return;
    }

    // Configurar los valores en los campos del formulario
    document.getElementById('descripcion_editar').value = descripcion;
    document.getElementById('unidad_medida_editar').value = unidadMedida;
    document.getElementById('fecha_vencimiento_editar').value = fechaVencimiento;
    //document.getElementById('stock_actual_editar').value = stockActual;
    document.getElementById('stock_minimo_editar').value = stockMinimo;

    // Configurar dinámicamente el atributo 'action' del formulario
    const form = document.getElementById('form-actualizar-material');
    form.action = `/actualizar_material/${materialId}/`; // Ajusta la URL según tu configuración en `urls.py`

    // Mostrar el modal
    modal.style.display = 'flex';
}

//-----FUNCION DE ABRIR EL MODAL Y AGREGAR STOCK----//

function abrirModalAgregarStock(materialId, descripcion) {
    const modal = document.getElementById('modal-agregar-stock');
    if (!modal) {
        console.error("No se encontró el modal con ID 'modal-agregar-stock'.");
        return;
    }

    // Configurar el título o mostrar el material en el modal
    const descripcionField = document.getElementById('descripcion_material_agregar');
    if (descripcionField) {
        descripcionField.textContent = descripcion;
    }

    // Configurar dinámicamente el atributo 'action' del formulario
    const form = document.getElementById('form-agregar-stock');
    if (form) {
        form.action = `/agregar-stock/${materialId}/`; // Ajusta la URL según tu configuración en `urls.py`
    }

    // Mostrar el modal
    modal.style.display = 'flex';
}



//-----FUNCION DE ABRIR EL MODAL Y ELIMINAR MATERIAL----//
function abrirModalEliminarMaterial(materialId, descripcion) {
    const modal = document.getElementById("modal-eliminar-material");
    if (!modal) {
        console.error("No se encontró el modal con ID 'modal-eliminar-material'.");
        return;
    }

    // Actualizar contenido del modal
    document.getElementById("material-eliminar-descripcion").innerText = descripcion;

    // Actualizar el atributo 'action' del formulario
    const form = document.getElementById("form-eliminar-material");
    form.action = `/eliminar_material/${materialId}/`;

    // Mostrar el modal
    modal.style.display = "flex";
}



/*BUSQUE DE MATERIALES EN PROCEDIMIENTOS*/
function buscarMateriales() {
    const query = document.getElementById("busqueda-material").value.trim();

    if (query === "") {
        document.getElementById("tabla-resultados-materiales").innerHTML = "";
        return;
    }

    fetch(`/optopico/buscar-materiales/?q=${query}&limite=10`)
        .then(response => response.json())
        .then(datos => {
            const tablaResultados = document.getElementById("tabla-resultados-materiales");
            tablaResultados.innerHTML = "";

            if (datos.length === 0) {
                const filaVacia = document.createElement("tr");
                filaVacia.innerHTML = `
                    <td colspan="4" class="py-2 px-4 text-center text-gray-500">No se encontraron materiales</td>
                `;
                tablaResultados.appendChild(filaVacia);
                return;
            }

            datos.forEach(material => {
                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td class="py-2 px-4 border-r text-center">${material.id}</td>
                    <td class="py-2 px-4 border-r">${material.descripcion}</td>
                    <td class="py-2 px-4 border-r text-center">${material.unidad_medida}</td>
                    <td class="py-2 px-4 text-center">
                        <button class="bg-blue-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-500"
                            onclick="seleccionarMaterial(${material.id}, '${material.descripcion}', '${material.unidad_medida}')">
                            Seleccionar
                        </button>
                    </td>
                `;
                tablaResultados.appendChild(fila);
            });
        })
        .catch(error => console.error("Error:", error));
}

/**
 * Selecciona un material y lo agrega a la tabla.
 */
function seleccionarMaterial(id, descripcion, unidad) {
    const tabla = document.getElementById("tabla-materiales").querySelector("tbody");

    if (document.querySelector(`.input-material-${id}`)) {
        alert("El material ya ha sido seleccionado.");
        return;
    }

    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
        <td class="py-2 px-4 border-r text-center">${id}</td>
        <td class="py-2 px-4 border-r">${descripcion}</td>
        <td class="py-2 px-4 border-r text-center">
            <input type="number" value="1" min="1" class="cantidad-material">
        </td>
        <td class="py-2 px-4 text-center">
            <button class="bg-red-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-red-500"
                onclick="eliminarMaterial(this, ${id})">Eliminar</button>
        </td>
    `;
    tabla.appendChild(nuevaFila);

    const contenedorInputs = document.getElementById("contenedor-inputs-materiales");
    contenedorInputs.innerHTML += `
        <input type="hidden" name="materiales[]" value="${id}" class="input-material-${id}">
        <input type="hidden" name="cantidades_materiales[]" value="1" class="input-cantidad-${id}">
    `;

    nuevaFila.querySelector(".cantidad-material").addEventListener("input", function (e) {
        document.querySelector(`.input-cantidad-${id}`).value = e.target.value;
    });

    cerrarModal();
}

/**
 * Elimina un material de la tabla.
 */
function eliminarMaterial(button, id) {
    button.parentElement.parentElement.remove();
    const materialInput = document.querySelector(`.input-material-${id}`);
    const cantidadInput = document.querySelector(`.input-cantidad-${id}`);
    if (materialInput) materialInput.remove();
    if (cantidadInput) cantidadInput.remove();
}




// -------- GESTIÓN DE PROCEDIMIENTOS ESPECIALES -------- //

/**
 * Maneja la selección y adición de procedimientos especiales a la tabla.
 */
document.addEventListener("DOMContentLoaded", function () {
    // Verificar si el elemento "tipo-procedimiento-especial" existe en la página
    const selectTipoProcedimiento = document.getElementById("tipo-procedimiento-especial");

    if (!selectTipoProcedimiento) {
        // Si el elemento no existe, terminar el script
        return;
    }

    // Crear un contenedor para el valor adicional (oculto por defecto)
    const contenedorValorAdicional = document.createElement("div");
    contenedorValorAdicional.style.display = "none"; // Oculto inicialmente
    contenedorValorAdicional.innerHTML = `
        <label for="valor-adicional" style="display: block; margin-top: 8px;">
            Ingrese el valor para HGT:
        </label>
        <input type="number" id="valor-adicional" name="valor_adicional"
               style="width: 100%; border: 1px solid #d1d5db; border-radius: 4px; padding: 8px;"
               placeholder="Ingrese un valor">
    `;

    // Agregar el contenedor después del select
    selectTipoProcedimiento.parentElement.appendChild(contenedorValorAdicional);

    // Escuchar cambios en el select
    selectTipoProcedimiento.addEventListener("change", function () {
        if (selectTipoProcedimiento.value === "HGT") {
            contenedorValorAdicional.style.display = "block"; // Mostrar el campo adicional
        } else {
            contenedorValorAdicional.style.display = "none"; // Ocultar el campo adicional
            document.getElementById("valor-adicional").value = ""; // Limpiar el valor ingresado
        }
    });

    // Manejar el envío del formulario
    const formProcedimientoEspecial = document.getElementById("form-tipo-procedimiento-especial");
    if (formProcedimientoEspecial) {
        formProcedimientoEspecial.addEventListener("submit", function (event) {
            event.preventDefault();

            const tipoSeleccionado = selectTipoProcedimiento.value;
            const valorAdicional = document.getElementById("valor-adicional").value || null;

            // Validar si HGT requiere un valor
            if (tipoSeleccionado === "HGT" && !valorAdicional) {
                alert("Por favor, ingrese un valor para HGT.");
                return;
            }

            agregarFilaATablaProcedimientoEspecial(tipoSeleccionado, valorAdicional);

            cerrarModal("tipo-procedimiento-especial");
        });
    }
});

/**
 * Agrega una fila a la tabla de procedimientos especiales con los datos proporcionados.
 * @param {string} tipo - Tipo de procedimiento seleccionado.
 * @param {string|null} valorAdicional - Valor adicional si aplica (solo para HGT).
 */
function agregarFilaATablaProcedimientoEspecial(tipo, valorAdicional) {
    const tabla = document.getElementById("tabla-tipo-procedimiento-especial")?.querySelector("tbody");

    if (!tabla) {
        console.error("La tabla de procedimientos especiales no se encontró o no tiene un cuerpo <tbody>.");
        return;
    }

    const filas = tabla.getElementsByTagName("tr").length;
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
        <td class="py-2 px-4 border-r text-center">${filas + 1}</td>
        <td class="py-2 px-4 border-r text-center">${tipo}</td>
        <td class="py-2 px-4 border-r text-center">${valorAdicional || "N/A"}</td>
        <td class="py-2 px-4 text-center">
            <button class="bg-red-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-red-500"
                    onclick="eliminarFilaProcedimientoEspecial(this)">Eliminar</button>
        </td>
    `;

    tabla.appendChild(nuevaFila);

    const formulario = document.querySelector("form");
    if (formulario) {
        formulario.innerHTML += `
            <input type="hidden" name="procedimientos_especiales[]" value="${tipo}">
            <input type="hidden" name="valores_adicionales[]" value="${valorAdicional || ""}">
        `;
    } else {
        console.error("No se encontró el formulario para agregar los inputs ocultos.");
    }
}

/**
 * Elimina una fila de la tabla de procedimientos especiales.
 * @param {HTMLButtonElement} button - El botón que se hizo clic para eliminar la fila.
 */
function eliminarFilaProcedimientoEspecial(button) {
    const fila = button.parentElement.parentElement;
    fila.remove();
}



// -------- GESTIÓN DE PROCEDIMIENTOS MÉDICOS -------- //

document.addEventListener("DOMContentLoaded", function () {
    const selectTipoProcedimiento = document.getElementById("tipo-procedimiento-medicos");
    const contenedorDescripcionOtros = document.createElement("div");
    contenedorDescripcionOtros.style.display = "none"; // Oculto por defecto
    contenedorDescripcionOtros.innerHTML = `
        <label for="descripcion-otros" style="display: block; margin-top: 8px;">
            Ingrese la descripción de "Otros":
        </label>
        <input type="text" id="descripcion-otros" name="descripcion_otros" 
               style="width: 100%; border: 1px solid #d1d5db; border-radius: 4px; padding: 8px;"
               placeholder="Ingrese una descripción">
    `;
    if (!selectTipoProcedimiento) {
        // Si el elemento no existe, terminar el script
        return;
    }
    // Agregar el contenedor después del select
    selectTipoProcedimiento.parentElement.appendChild(contenedorDescripcionOtros);

    // Escuchar cambios en el select
    selectTipoProcedimiento.addEventListener("change", function () {
        if (selectTipoProcedimiento.value === "OTROS") {
            contenedorDescripcionOtros.style.display = "block"; // Mostrar campo adicional
        } else {
            contenedorDescripcionOtros.style.display = "none"; // Ocultar campo adicional
            document.getElementById("descripcion-otros").value = ""; // Limpiar el valor ingresado
        }
    });

    // Manejar el envío del formulario
    const formProcedimientoMedicos = document.getElementById("form-tipo-procedimiento-medicos");
    if (formProcedimientoMedicos) {
        formProcedimientoMedicos.addEventListener("submit", function (event) {
            event.preventDefault();

            const tipoSeleccionado = selectTipoProcedimiento.value;
            let descripcion = tipoSeleccionado;

            // Si selecciona "OTROS", usar el valor ingresado en el campo de descripción
            if (tipoSeleccionado === "OTROS") {
                const descripcionOtros = document.getElementById("descripcion-otros").value.trim();
                if (!descripcionOtros) {
                    alert("Por favor, ingrese una descripción para 'Otros'.");
                    return;
                }
                descripcion = descripcionOtros;
            }

            agregarFilaATablaProcedimientoMedico(tipoSeleccionado, descripcion);
            cerrarModal("tipo-procedimiento-medicos");
        });
    }
});

/**
 * Agrega una nueva fila a la tabla de procedimientos médicos.
 * @param {string} tipo - Tipo de procedimiento seleccionado.
 * @param {string} descripcion - Descripción personalizada o tipo seleccionado.
 */
function agregarFilaATablaProcedimientoMedico(tipo, descripcion) {
    const tabla = document.getElementById("tabla-tipo-procedimiento-medicos")?.querySelector("tbody");

    if (!tabla) {
        console.error("La tabla de procedimientos médicos no se encontró o no tiene un cuerpo <tbody>.");
        return;
    }

    const filas = tabla.getElementsByTagName("tr").length;
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
        <td class="py-2 px-4 border-r text-center">${filas + 1}</td>
        <td class="py-2 px-4 border-r text-center">${descripcion}</td>
        <td class="py-2 px-4 text-center">
            <button class="bg-red-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-red-500"
                    onclick="eliminarFilaProcedimientoMedico(this)">Eliminar</button>
        </td>
    `;

    tabla.appendChild(nuevaFila);

    const formulario = document.querySelector("form");
    if (formulario) {
        formulario.innerHTML += `
            <input type="hidden" name="procedimientos_medicos[]" value="${tipo}">
            <input type="hidden" name="descripciones_medicos[]" value="${descripcion}">
        `;
    } else {
        console.error("No se encontró el formulario para agregar los inputs ocultos.");
    }
}

/**
 * Elimina una fila de la tabla de procedimientos médicos.
 * @param {HTMLButtonElement} button - El botón que se hizo clic para eliminar la fila.
 */
function eliminarFilaProcedimientoMedicos(button) {
    const fila = button.parentElement.parentElement;
    fila.remove();
}



// -------- CURACION DE HERIDAS -------- //

document.addEventListener("DOMContentLoaded", function () {
    const formCuracionHerida = document.getElementById("form-tipo-curacion");

    if (formCuracionHerida) {
        formCuracionHerida.addEventListener("submit", function (event) {
            event.preventDefault();

            const tiempo = document.getElementById("tipo-curacion1").value;
            const complejidad = document.getElementById("tipo-curacion2").value;
            const fase = document.getElementById("tipo-curacion3").value;
            const tipoCuracion = document.getElementById("tipo-curacion4").value;

            if (!tiempo || !complejidad || !fase || !tipoCuracion) {
                alert("Todos los campos son obligatorios para agregar una curación.");
                return;
            }

            agregarFilaATablaCuracionHerida(tiempo, complejidad, fase, tipoCuracion);
            cerrarModal("tipo-curacion");
        });
    }
});

/**
 * Agrega una fila a la tabla de curación de heridas.
 * @param {string} tiempo - Tipo de herida por tiempo.
 * @param {string} complejidad - Complejidad de la herida.
 * @param {string} fase - Fase de la herida.
 * @param {string} tipoCuracion - Tipo de curación (simple o avanzada).
 */
function agregarFilaATablaCuracionHerida(tiempo, complejidad, fase, tipoCuracion) {
    const tabla = document.getElementById("tabla-tipo-curacion").querySelector("tbody");

    if (!tabla) {
        console.error("La tabla de curación de heridas no se encontró o no tiene un cuerpo <tbody>.");
        return;
    }

    const filas = tabla.getElementsByTagName("tr").length;
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
        <td class="py-2 px-4 border-r text-center">${filas + 1}</td>
        <td class="py-2 px-4 border-r text-center">${tiempo}</td>
        <td class="py-2 px-4 border-r text-center">${complejidad}</td>
        <td class="py-2 px-4 border-r text-center">${fase}</td>
        <td class="py-2 px-4 border-r text-center">${tipoCuracion}</td>
        <td class="py-2 px-4 text-center">
            <button class="bg-red-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-red-500"
                    onclick="eliminarFilaCuracionHerida(this)">Eliminar</button>
        </td>
    `;

    tabla.appendChild(nuevaFila);

    const formulario = document.querySelector("form");
    if (formulario) {
        formulario.innerHTML += `
            <input type="hidden" name="curacion_tiempo[]" value="${tiempo}">
            <input type="hidden" name="curacion_complejidad[]" value="${complejidad}">
            <input type="hidden" name="curacion_fase[]" value="${fase}">
            <input type="hidden" name="curacion_tipo[]" value="${tipoCuracion}">
        `;
    } else {
        console.error("No se encontró el formulario para agregar los inputs ocultos.");
    }
}

/**
 * Elimina una fila específica de la tabla de curación de heridas.
 * @param {HTMLButtonElement} button - El botón que se hizo clic para eliminar la fila.
 */
function eliminarFilaCuracionHerida(button) {
    const fila = button.parentElement.parentElement;
    fila.remove();
}


// -------- DIAGNOSTICO MEDICOS -------- //

document.addEventListener("DOMContentLoaded", function () {
    const formDiagnosticoMedico = document.getElementById("form-tipo-diagnostico");

    if (formDiagnosticoMedico) {
        formDiagnosticoMedico.addEventListener("submit", function (event) {
            event.preventDefault();

            const diagnosticoSelect = document.getElementById("tipo-diagnostico");
            const diagnosticoId = diagnosticoSelect.value;
            const diagnosticoDescripcion = diagnosticoSelect.options[diagnosticoSelect.selectedIndex].text;

            if (!diagnosticoId) {
                alert("Por favor, seleccione un diagnóstico médico.");
                return;
            }

            agregarFilaATablaDiagnosticoMedico(diagnosticoId, diagnosticoDescripcion);
            cerrarModal("tipo-diagnostico");
        });
    }
});

/**
 * Agrega una fila a la tabla de diagnósticos médicos.
 * @param {string} diagnosticoId - ID del diagnóstico médico seleccionado.
 * @param {string} diagnosticoDescripcion - Descripción del diagnóstico médico seleccionado.
 */
function agregarFilaATablaDiagnosticoMedico(diagnosticoId, diagnosticoDescripcion) {
    const tabla = document.getElementById("tabla-medicamento").querySelector("tbody");

    if (!tabla) {
        console.error("La tabla de diagnósticos médicos no se encontró o no tiene un cuerpo <tbody>.");
        return;
    }

    // Verificar si el diagnóstico ya ha sido seleccionado
    if (document.querySelector(`.input-diagnostico-${diagnosticoId}`)) {
        alert("El diagnóstico médico ya ha sido seleccionado.");
        return;
    }

    const filas = tabla.getElementsByTagName("tr").length;
    const nuevaFila = document.createElement("tr");
    nuevaFila.innerHTML = `
        <td class="py-2 px-4 border-r text-center">${filas + 1}</td>
        <td class="py-2 px-4 border-r text-center">${diagnosticoDescripcion}</td>
        <td class="py-2 px-4 text-center">
            <button class="bg-red-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-red-500"
                    onclick="eliminarFilaDiagnosticoMedico(this)">Eliminar</button>
        </td>
    `;

    tabla.appendChild(nuevaFila);

    const formulario = document.querySelector("form");
    if (formulario) {
        formulario.innerHTML += `
            <input type="hidden" name="diagnosticos[]" value="${diagnosticoId}" class="input-diagnostico-${diagnosticoId}">
        `;
    } else {
        console.error("No se encontró el formulario para agregar los inputs ocultos.");
    }
}

/**
 * Elimina una fila de la tabla de diagnósticos médicos.
 * @param {HTMLButtonElement} button - El botón que se hizo clic para eliminar la fila.
 */
function eliminarFilaDiagnosticoMedico(button) {
    const fila = button.parentElement.parentElement;
    fila.remove();

    // Eliminar el input oculto correspondiente
    const diagnosticoId = fila.querySelector("input[name='diagnosticos[]']").value;
    const inputOculto = document.querySelector(`.input-diagnostico-${diagnosticoId}`);
    if (inputOculto) inputOculto.remove();
}
