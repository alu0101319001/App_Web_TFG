// frontend/static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const filtros = document.querySelectorAll('#filtros .form-check-input');
    filtros.forEach(filtro => {
      filtro.addEventListener('change', function() {
        aplicarFiltros();
      });
    });
  });
  
  function aplicarFiltros() {
    const filtros = document.querySelectorAll('#filtros .form-check-input');
    const ordenadores = document.querySelectorAll('.icono-ordenador');
    
    ordenadores.forEach(ordenador => {
      let mostrar = true;
      filtros.forEach(filtro => {
        if (filtro.checked) {
          if (ordenador.dataset.estado !== filtro.value) {
            mostrar = false;
          }
        }
      });
      ordenador.style.display = mostrar ? 'block' : 'none';
    });
  }
  
  function ejecutarAccion(accion) {
    const ordenadores = document.querySelectorAll('.icono-ordenador');
    ordenadores.forEach(ordenador => {
      if (ordenador.style.display === 'block') {
        console.log(`Ejecutando ${accion} en ${ordenador.dataset.nombre}`);
        // Aquí puedes añadir la lógica para ejecutar la acción en el ordenador
      }
    });
  }
  