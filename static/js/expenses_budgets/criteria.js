$(document).ready(() => {

  $(document).on('keyup', '.percentaje_ppto', function () {
    let criteria = $(this).closest('tr').find('.budget_table_select').val();
    let value = parseFloat($(this).val());
    let dicAmount = parseFloat($(this).data('dic'));
    let div = value / 100;
    let amount = dicAmount * div;

    if (criteria === '2') {
      let result = numberWithCommas((amount + dicAmount).toFixed(2));
      $(this).closest('tr').find('.total_ppto').val(result);
    } else if (criteria === '4') {
      let result = numberWithCommas((dicAmount - amount).toFixed(2));
      $(this).closest('tr').find('.total_ppto').val(result);
    }
  });

  $('.budget_table_select').change(function () {
    let criteria = $(this).val();
    let novAmount = parseFloat($(this).data('nov'));
    let dicAmount = parseFloat($(this).data('dic'));
    let value = parseFloat(
      $(this).children(":selected").attr("data-valor")
    ).toFixed(2);

    if (criteria === '1') {
      let amount = dicAmount * value / 100;
      let result = numberWithCommas((dicAmount + amount).toFixed(2));
      $(this).closest('tr').find('.percentaje_ppto').attr('readonly', true).val(value);
      $(this).closest('tr').find('.total_ppto').val(result);
      $(this).closest('tr').find('.justificacion_ppto').attr('readonly', true).val('');

    } else if (criteria === '2') {
      $(this).closest('tr').find('.percentaje_ppto').attr('readonly', false).val('0');
      $(this).closest('tr').find('.total_ppto').attr('readonly', true).val('0');
      $(this).closest('tr').find('.justificacion_ppto').attr('readonly', false);

    } else if (criteria === '3') {
      $(this).closest('tr').find('.percentaje_ppto').attr('readonly', true).val(0);
      $(this).closest('tr').find('.total_ppto').val(numberWithCommas(dicAmount));
      $(this).closest('tr').find('.justificacion_ppto').attr('readonly', false).val('');

    } else if (criteria === '4') {
      $(this).closest('tr').find('.percentaje_ppto').attr('readonly', false).val('0');
      $(this).closest('tr').find('.total_ppto').attr('readonly', true).val('0');
      $(this).closest('tr').find('.justificacion_ppto').attr('readonly', false).val('');

    } else if (criteria === '5') {
      $(this).closest('tr').find('.percentaje_ppto').attr('readonly', true).val('');
      $(this).closest('tr').find('.total_ppto').attr('readonly', true).val(0);
      $(this).closest('tr').find('.justificacion_ppto').attr('readonly', true).val('');

    } else if (criteria === '6') {
      $(this).closest('tr').find('.percentaje_ppto').attr('readonly', true).val('');
      $(this).closest('tr').find('.total_ppto').attr('readonly', false).val(0);
      $(this).closest('tr').find('.justificacion_ppto').attr('readonly', false).val('');

    }
  });
});