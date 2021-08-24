$('.validation-input-text').keydown(function (event) {
  if (event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 190 || event.keyCode == 110
    || event.keyCode == 27 || event.keyCode == 13
    || (event.keyCode == 65 && event.ctrlKey === true)
    || (event.keyCode >= 35 && event.keyCode <= 39)) {
    return;
  } else {
    if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105)) {
      event.preventDefault();
    }
  }
});


const numberWithCommas = (x)=> {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


$(".validation-input-text, .validation-number-input-text").keyup(function(event){
  var valor = $(this).val();
  valor =  valor.replace(/,/g, '');
  $(this).val(numberWithCommas(valor));
});