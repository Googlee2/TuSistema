// Tomamos todas las ventas
const ventas = getVentas();

/* ===== VENTAS POR DÍA ===== */
function ventasPorDia() {
  const dias = {};
  ventas.forEach(v => {
    dias[v.fecha] = (dias[v.fecha] || 0) + v.total;
  });
  return dias;
}

/* ===== VENTAS POR CATEGORÍA ===== */
function ventasPorCategoria() {
  const categorias = {};
  ventas.forEach(v => {
    categorias[v.categoria] = (categorias[v.categoria] || 0) + v.total;
  });
  return categorias;
}

/* ===== DIBUJAR BARRAS ===== */
function dibujarBarras() {
  const contenedor = document.getElementById("bars");
  if (!contenedor) return;

  contenedor.innerHTML = "";
  const datos = ventasPorDia();
  const max = Math.max(...Object.values(datos));

  Object.entries(datos).forEach(([dia, total]) => {
    const barra = document.createElement("div");
    barra.className = "bar";
    barra.style.height = (total / max * 100) + "%";
    barra.textContent = total;
    barra.title = `${dia}: $${total}`;
    contenedor.appendChild(barra);
  });
}

/* ===== DIBUJAR TORTA ===== */
function dibujarTorta() {
  const pie = document.getElementById("pie");
  if (!pie) return;

  const datos = ventasPorCategoria();
  const total = Object.values(datos).reduce((a, b) => a + b, 0);

  let gradiente = "";
  let acumulado = 0;

  Object.values(datos).forEach(valor => {
    const pct = (valor / total) * 100;
    const color = `hsl(${Math.random() * 360}, 70%, 50%)`;
    gradiente += `${color} ${acumulado}% ${acumulado + pct}%,`;
    acumulado += pct;
  });

  pie.style.background = `conic-gradient(${gradiente.slice(0, -1)})`;
}

/* ===== INICIALIZAR ===== */
document.addEventListener("DOMContentLoaded", () => {
  dibujarBarras();
  dibujarTorta();
});
