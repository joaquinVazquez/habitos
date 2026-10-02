let habitoAEliminar = null;

function abrirConfirmacionEliminar(boton) {
  habitoAEliminar = {
    id: boton.dataset.habitoId,
    nombre: boton.dataset.habitoNombre,
  };
  document.getElementById("modal-eliminar-nombre").textContent = habitoAEliminar.nombre;
  document.getElementById("modal-eliminar").classList.add("is-open");
}

function cerrarConfirmacionEliminar() {
  habitoAEliminar = null;
  document.getElementById("modal-eliminar").classList.remove("is-open");
}

// --- Editar hábito ---
function abrirEdicionHabito(boton) {
  document.getElementById("editar-nombre").value = boton.dataset.habitoNombre;
  document.getElementById("editar-descripcion").value = boton.dataset.habitoDescripcion;
  document.getElementById("form-editar").dataset.habitoId = boton.dataset.habitoId;
  document.getElementById("editar-error").innerHTML = "";
  document.getElementById("modal-editar").classList.add("is-open");
}

function cerrarEdicionHabito() {
  document.getElementById("modal-editar").classList.remove("is-open");
}

document.addEventListener("DOMContentLoaded", () => {
  // Confirmar eliminación
  document.getElementById("btn-confirmar-eliminar").addEventListener("click", () => {
    if (!habitoAEliminar) return;
    const { id } = habitoAEliminar;

    htmx.ajax("DELETE", `/habitos/${id}`, {
      target: `#habito-${id}`,
      swap: "outerHTML swap:200ms",
    });

    cerrarConfirmacionEliminar();
  });

  // Guardar edición
  const formEditar = document.getElementById("form-editar");
  formEditar.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const id = formEditar.dataset.habitoId;
    const datos = new FormData(formEditar);

    const respuesta = await fetch(`/habitos/${id}`, {
      method: "PUT",
      body: datos,
    });

    const html = await respuesta.text();

    if (respuesta.ok) {
      const tarjetaVieja = document.getElementById(`habito-${id}`);
      tarjetaVieja.outerHTML = html;
      // La tarjeta se insertó como HTML plano, no vía HTMX, así que hay
      // que decirle a HTMX que la procese para que el botón "cumplido hoy"
      // (que usa hx-post) funcione en la tarjeta nueva.
      htmx.process(document.getElementById(`habito-${id}`));
      cerrarEdicionHabito();
    } else {
      document.getElementById("editar-error").innerHTML = html;
    }
  });

  // Cerrar cualquier modal con Escape
  document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape") {
      cerrarConfirmacionEliminar();
      cerrarEdicionHabito();
      document.getElementById("modal-crear")?.classList.remove("is-open");
    }
  });
});

// --- Toast flotante para el mensaje motivacional de IA ---
function mostrarToast(mensaje, esError = false) {
  const contenedor = document.getElementById("toast-container");

  const toast = document.createElement("div");
  toast.className = "toast" + (esError ? " toast--error" : "");
  toast.textContent = mensaje;
  contenedor.appendChild(toast);

  // requestAnimationFrame asegura que el navegador pinte el estado inicial
  // antes de añadir la clase que dispara la transición de entrada.
  requestAnimationFrame(() => toast.classList.add("toast--visible"));

  setTimeout(() => {
    toast.classList.remove("toast--visible");
    toast.addEventListener("transitionend", () => toast.remove(), { once: true });
  }, 8000);
}