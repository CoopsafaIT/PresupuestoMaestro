$(document).ready(() => {
  $('.save_budget_item').click(function (e) {
    e.preventDefault()
    e.stopPropagation()
    id = $(this).attr('id');
    let url = $('#id_urls').data('budget-register');
    let criteria = $(this).closest('tr').find('.criterio_ppto').val();
    let justification = $(this).closest('tr').find('.justificacion_ppto').val();
    let total_amount = $(this).closest('tr').find('.total_ppto').val();

    if ((justification == '' && criteria == '2') || (justification == '' && criteria == '6')) {
      alert('¡Agregue una justificación!');
    } else {
      let linea = document.getElementById(id);
      let id_budget = $(this).attr('data-id');
      let cost_center = $('#id_cost_centers option:selected').val()
      let period = $('#id_periods option:selected').val()
      let project = $('#id_project option:selected').val()

      $.ajax({
        type: "POST",
        data: {
          cost_center: cost_center,
          criteria: criteria,
          justification: justification,
          id_budget: id_budget,
          period: period,
          project: project,
          total_amount: total_amount,
        },
        url: url
      })
        .done(response)
        .fail(handleSaveError)
    }
  });

  const response = (resp) => {
    let totals = resp.result[0].Totales
    let status_one = resp.result[0].Presupuestada
    if (totals == status_one) {
      $('#aprobacion').removeAttr('disabled');
    }

    if (resp.data[0].estado == 1) {
      $(`*[data-td="td-id-${resp.data[0].pk}"]`).addClass('td-border-success');
    }
  }

  const handleSaveError = (e) => {
    console.log(e);
    alert("No se pudo guardar correctamente linea presupuestaria")
  }
})