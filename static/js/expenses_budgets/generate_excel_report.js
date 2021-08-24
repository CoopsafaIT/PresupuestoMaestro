$('#btn-generate-report').click((e) => {
  e.stopPropagation()
  e.preventDefault();
  let cost_center = $('#id_cost_centers').val();
  let project = $('#id_project').val();
  let period = $('#id_periods').val();
  if (cost_center === '') alert("Seleccione Centro de costo para generar reporte")
  else if (project === '') alert("Seleccione Proyecto para generar reporte")
  else if (period === '') alert("Seleccione Periodo para generar reporte")
  else {
    let url = `/expenses-budgets/generate-excel-report/${project}/${period}/${cost_center}/`
    window.open(url, '_blank').focus();
  }
})