function render_analysis(text) {
  var loading = '<div class="d-flex justify-content-center"><div class="spinner-border text-primary" role="status"><span class="sr-only">Loading...</span></div></div>';
  $('#analysis').html(loading);
  $.post('/analyze', text, function(data) {
    $('#analysis').html(data);
  });
}

function readUrl(input) {
  if (input.files && input.files[0]) {
    let reader = new FileReader();
    reader.onload = (e) => {
      render_analysis(reader.result);
    }
    reader.readAsText(input.files[0]);
  }
}