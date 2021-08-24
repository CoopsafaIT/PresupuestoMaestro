$(document).ready(() => {
  $('#id_periods, #id_cost_centers').change(() => getProjects());

  const getProjects = () => {
    let url = $('#id_urls').data('get_projects');
    if ($('#id_periods').val() !== '' && $('#id_cost_centers').val() !== '') {
      $('#btn-generate-report').show();
    }
    if ($('#id_cost_centers').val() !== '') {
      let cost_center_id = $('#id_cost_centers').val();
      $.ajax({
        type: 'GET',
        data: {
          cost_center_id: cost_center_id
        },
        url: url
      })
        .done(fillSelected)
        .fail(handleError)
    }
  }

  const fillSelected = (resp) => {
    let project_session = $('#id_var').data('project_session');
    $('#id_project').empty();
    $('#id_project').append('<option value="">--- Seleccione Proyecto ---</option>');
    $.each(resp, (key, val) => {
      $('#id_project').append(`<option value=${val.codproyecto}>${val.descproyecto}</option>`);
    })
    $('#id_project').trigger("chosen:updated");
    $(
      `#id_project option[value= '${project_session}'] `
    ).prop('selected', true).trigger("change");
  }

  const handleError = (e) => {
    console.log(e);
    alert("No se pudo Cargar Proyectos asociados al centro de costos!")
  }

  setTimeout(() => {
    getProjects();
  }, 2000);

  $('#btn-create-project').click(function () {
    let url = $('#id_urls').data('create_project');
    let cost_center = $('#id_cost_centers option:selected').val()
    let project_desc = $('#project_desc_id').val()
    let date_start = $('#project_date_start_id').val()
    let date_end = $('#project_date_end_id').val()
    if (cost_center === '' || project_desc === '' || date_end === '' || date_start === '') {
      alert('Seleccione centro de costo y ingrese campos del formulario')
      return
    }

    $.ajax({
      type: 'POST',
      data: {
        cost_center,
        project_desc,
        date_end,
        date_start
      },
      url: url
    })
      .done(successCreateProject)
      .fail(handleErrorCreateProject)
  });

  const successCreateProject = (resp) => {
    getProjects();
    alert('Proyecto creado con éxito')
  }

  const handleErrorCreateProject = (err) => {
    console.log(err);
    alert('No se pudo crear project por favor valide campos ingresados y intente de nuevo')
  }

})