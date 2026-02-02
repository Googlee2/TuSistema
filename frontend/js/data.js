/*
  Estructura de venta:
  {
    fecha: "2026-02-01",
    total: 15000,
    categoria: "Alimentos"
  }
*/

// Devuelve todas las ventas
function getVentas() {
  return JSON.parse(localStorage.getItem("ventas")) || [];
}

// Guarda una venta nueva
function guardarVenta(venta) {
  const ventas = getVentas();
  ventas.push(venta);
  localStorage.setItem("ventas", JSON.stringify(ventas));
}

// Datos de prueba (solo la primera vez)
if (!localStorage.getItem("ventas")) {
  const demo = [
    { fecha: "2026-02-01", total: 15000, categoria: "Alimentos" },
    { fecha: "2026-02-01", total: 8000, categoria: "Bebidas" },
    { fecha: "2026-02-02", total: 12000, categoria: "Limpieza" },
    { fecha: "2026-02-03", total: 18000, categoria: "Alimentos" },
    { fecha: "2026-02-03", total: 6000, categoria: "Otros" }
  ];
  localStorage.setItem("ventas", JSON.stringify(demo));
}
