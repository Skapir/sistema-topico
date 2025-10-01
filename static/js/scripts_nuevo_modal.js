// Mostrar un modal específico 
function mostrarModal(idModal) {
  const modal = document.getElementById(`modal-${idModal}`);
  if (modal) {
    modal.style.display = "flex"; // Mostrar el modal al hacer clic
  } else {
    console.error(`No se encontró el modal con ID modal-${idModal}`);
  }
}

// Cerrar todos los modales
function cerrarModal() {
  const modales = document.querySelectorAll('[id^="modal-"]');
  modales.forEach((modal) => (modal.style.display = "none"));
}


// Asegurar que al cargar la página, todos los modales estén ocultos
document.addEventListener("DOMContentLoaded", function () {
  const modales = document.querySelectorAll('[id^="modal-"]');
  modales.forEach((modal) => (modal.style.display = "none")); // Ocultar todos los modales
});

// -------- TIPO DE PROCEDIMIENTO -------- //

// Mapeo de nombres completos para Tipo de Procedimiento
const tipoProcedimientoCompleto = {
  IM: "Intramuscular",
  SC: "Subcutáneo",
  VIAEV: "Vía Endovenosa",
  ID: "Intradérmico",
};

// Capturar el formulario de Tipo de Procedimiento y agregar fila
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("form-tipo-procedimiento");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();

      // Capturar el valor seleccionado del tipo de procedimiento
      const tipoSeleccionado = document.getElementById("tipo-procedimiento").value;

      // Obtener el nombre completo
      const nombreCompleto = tipoProcedimientoCompleto[tipoSeleccionado] || tipoSeleccionado;

      // Actualizar el campo oculto en el formulario principal
      const descripcionInput = document.getElementById("descripcion-procedimiento");
      descripcionInput.value = nombreCompleto;

      // Agregar fila a la tabla
      agregarFilaATablaProcedimiento(tipoSeleccionado, nombreCompleto);

      // Cerrar el modal
      cerrarModal();
    });
  } else {
    console.error("El formulario con ID 'form-tipo-procedimiento' no se encontró en el DOM.");
  }
});


// Agregar fila a la tabla de Tipo de Procedimiento
function agregarFilaATablaProcedimiento(tipo, descripcion) {
  const tabla = document.getElementById("tabla-tipo-procedimiento").querySelector("tbody");

  if (!tabla) {
    console.error("La tabla no se encontró o no tiene un cuerpo <tbody>.");
    return;
  }

  // Contar las filas existentes
  const filas = tabla.getElementsByTagName("tr").length;

  // Crear nueva fila
  const nuevaFila = document.createElement("tr");
  nuevaFila.innerHTML = `
    <td class="py-2 px-4 border-r text-center">${filas + 1}</td>
    <td class="py-2 px-4 border-r text-center">${descripcion}</td>
    <td class="py-2 px-4 text-center">
      <button class="bg-red-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-red-500"
        onclick="eliminarFilaProcedimiento(this)">Eliminar</button>
    </td>
  `;

  // Agregar la fila a la tabla
  tabla.appendChild(nuevaFila);

  // Agregar inputs ocultos al formulario principal
  const formulario = document.querySelector("form");
  formulario.innerHTML += `
    <input type="hidden" name="procedimientos[]" value="${tipo}" class="input-procedimiento-${filas + 1}">
    <input type="hidden" name="descripciones[]" value="${descripcion}" class="input-descripcion-${filas + 1}">
  `;
}


// Función para eliminar la fila de la tabla y los inputs ocultos asociados
function eliminarFilaProcedimiento(button) {
  const fila = button.parentElement.parentElement; // Fila de la tabla
  const index = Array.from(fila.parentElement.children).indexOf(fila) + 1; // Índice de la fila

  // Eliminar la fila de la tabla
  fila.remove();

  // Eliminar inputs ocultos asociados en el formulario principal
  const inputProcedimiento = document.querySelector(`.input-procedimiento-${index}`);
  const inputDescripcion = document.querySelector(`.input-descripcion-${index}`);
  if (inputProcedimiento) inputProcedimiento.remove();
  if (inputDescripcion) inputDescripcion.remove();
}

// -------- MEDICAMENTOS -------- //
// Buscar medicamentos en tiempo real
function buscarMedicamentos() {
  const query = document.getElementById("busqueda-medicamento").value.trim();

  // Si no hay texto, limpia los resultados
  if (query === "") {
    document.getElementById("tabla-resultados-medicamentos").innerHTML = "";
    return;
  }

  // Hacer la solicitud al servidor
  fetch(`/optopico/buscar-medicamentos/?q=${query}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error al obtener los datos");
      }
      return response.json();
    })
    .then((datos) => {
      const tablaResultados = document.getElementById("tabla-resultados-medicamentos");

      // Limpiar la tabla antes de mostrar nuevos resultados
      tablaResultados.innerHTML = "";

      // Si no hay resultados, mostrar un mensaje
      if (datos.length === 0) {
        const filaVacia = document.createElement("tr");
        filaVacia.innerHTML = `
                  <td colspan="4" class="py-2 px-4 text-center text-gray-500">No se encontraron medicamentos</td>
              `;
        tablaResultados.appendChild(filaVacia);
        return;
      }

      // Recorrer los datos y agregarlos a la tabla
      datos.forEach((medicamento) => {
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
    .catch((error) => {
      console.error("Error:", error);
    });
}


// Función para agregar medicamentos seleccionados
function seleccionarMedicamento(id, descripcion, unidad) {
  const tabla = document.getElementById("tabla-medicamento").querySelector("tbody");

  // Verificar si el medicamento ya está seleccionado
  if (document.querySelector(`.input-medicamento-${id}`)) {
    alert("El medicamento ya ha sido seleccionado.");
    return;
  }

  // Crear una fila en la tabla
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

  // Agregar un input oculto con el ID del medicamento
  const contenedorInputs = document.getElementById("contenedor-inputs-medicamentos");
  contenedorInputs.innerHTML += `<input type="hidden" name="medicamentos[]" value="${id}" class="input-medicamento-${id}">`;

  cerrarModal();
}

// Función para eliminar medicamentos seleccionados
function eliminarMedicamento(button, id) {
  // Eliminar la fila de la tabla
  button.parentElement.parentElement.remove();

  // Eliminar el input oculto correspondiente
  const input = document.querySelector(`.input-medicamento-${id}`);
  if (input) input.remove();
}

// -------- MATERIALES E INSUMOS -------- //
// Cargar datos de Materiales e Insumos
function buscarMateriales() {
  const query = document.getElementById("busqueda-material").value.trim();

  // Si no hay texto, limpia los resultados
  if (query === "") {
    document.getElementById("tabla-resultados-materiales").innerHTML = "";
    return;
  }

  // Hacer la solicitud al servidor
  fetch(`/optopico/buscar-materiales/?q=${query}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error al obtener los datos");
      }
      return response.json();
    })
    .then((datos) => {
      const tablaResultados = document.getElementById("tabla-resultados-materiales");

      // Limpiar la tabla antes de mostrar nuevos resultados
      tablaResultados.innerHTML = "";

      // Si no hay resultados, mostrar un mensaje
      if (datos.length === 0) {
        const filaVacia = document.createElement("tr");
        filaVacia.innerHTML = `
                  <td colspan="4" class="py-2 px-4 text-center text-gray-500">No se encontraron materiales</td>
              `;
        tablaResultados.appendChild(filaVacia);
        return;
      }

      // Recorrer los datos y agregarlos a la tabla
      datos.forEach((material) => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
                  <td class="py-2 px-4 border-r text-center">${material.id}</td>
                  <td class="py-2 px-4 border-r">${material.descripcion}</td>
                  <td class="py-2 px-4 border-r text-center">${material.fecha_vencimiento}</td>
                  <td class="py-2 px-4 text-center">
                      <button class="bg-blue-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-blue-500"
                          onclick="seleccionarMaterial(${material.id}, '${material.descripcion}', '${material.unidad_medida}', '${material.fecha_vencimiento}')">
                          Seleccionar
                      </button>
                  </td>
              `;
        tablaResultados.appendChild(fila);
      });
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}


// Función para agregar materiales seleccionados
function seleccionarMaterial(id, descripcion) {
  const tabla = document.getElementById("tabla-materiales").querySelector("tbody");

  // Verificar si el material ya está seleccionado
  if (document.querySelector(`.input-material-${id}`)) {
    alert("El material ya ha sido seleccionado.");
    return;
  }

  // Crear una fila en la tabla
  const nuevaFila = document.createElement("tr");
  nuevaFila.innerHTML = `
    <td class="py-2 px-4 border-r text-center">${id}</td>
    <td class="py-2 px-4 border-r">${descripcion}</td>
    <td class="py-2 px-4 border-r text-center">
      <input type="number" value="1" min="1" class="w-16 text-center border rounded-md cantidad-material">
    </td>
    <td class="py-2 px-4 text-center">
      <button class="bg-red-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-red-500"
        onclick="eliminarMaterial(this, ${id})">Eliminar</button>
    </td>
  `;
  tabla.appendChild(nuevaFila);

  // Agregar inputs ocultos con el ID del material y la cantidad
  const contenedorInputs = document.getElementById("contenedor-inputs-materiales");
  contenedorInputs.innerHTML += `
    <input type="hidden" name="materiales[]" value="${id}" class="input-material-${id}">
    <input type="hidden" name="cantidades_materiales[]" value="1" class="input-cantidad-${id}">
  `;

  // Actualizar el input oculto de cantidad cuando cambie el valor en la tabla
  nuevaFila.querySelector(".cantidad-material").addEventListener("input", (e) => {
    document.querySelector(`.input-cantidad-${id}`).value = e.target.value;
  });

  cerrarModal();
}

// Función para eliminar materiales seleccionados
function eliminarMaterial(button, id) {
  // Eliminar la fila de la tabla
  button.parentElement.parentElement.remove();

  // Eliminar los inputs ocultos correspondientes
  const materialInput = document.querySelector(`.input-material-${id}`);
  const cantidadInput = document.querySelector(`.input-cantidad-${id}`);
  if (materialInput) materialInput.remove();
  if (cantidadInput) cantidadInput.remove();
}

// -------- VALIDACIÓN FORMULARIO -------- //
document.querySelector("form").addEventListener("submit", function (event) {
  const medicamentos = document.querySelectorAll('input[name="medicamentos[]"]');
  const materiales = document.querySelectorAll('input[name="materiales[]"]');

  if (medicamentos.length === 0 && materiales.length === 0) {
    alert("Debes seleccionar al menos un medicamento o un material.");
    event.preventDefault();
  }
});



document.addEventListener("DOMContentLoaded", function () {
  const modalExito = document.getElementById("modal-exito");
  const showModalExito = document.body.dataset.showModalExito === "true";

  if (modalExito && showModalExito) {
    console.log("Modal de éxito activado");
    modalExito.classList.remove("hidden");
    modalExito.classList.add("flex");
  }
});

function cerrarModalExito() {
  const modal = document.getElementById("modal-exito");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
}







