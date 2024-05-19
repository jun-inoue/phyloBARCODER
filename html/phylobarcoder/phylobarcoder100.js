$(function() {
  $('#my_form').submit('click', function(e) {
    e.preventDefault();

    var consoleInfo = console.info($('#my_form').get(0).submit);
    console.log(consoleInfo)

    var fd = new FormData($('#my_form').get(0));

    //if (fd.get("input_file").size == 0) {
    //    fd.delete("input_file"); 
    //}

    //for (var key of fd.keys()) {
    //    console.log(key);
    // }

/*
    for (item of fd){
      console.log(item)
    }
*/

    $(document)
    .ajaxStart(function(){
      //$('#prog').show();
      //$('#result').html('<img src="loadingCircle.gif" alt="" />');
      $('#result').html('<img src="ThinStripes.gif" alt="" />');
    })
    console.log("test1")
    $.ajax({
      url: '/cgi-bin/phyloBARCODER100.py',
      type: 'post',
      dataType: 'text',
      data: fd,
      processData: false,
      contentType: false,
    })
    .done(function(response) {
      console.log("testDone")
      $('#result').html(response);
    })
    $(document)
    .ajaxError(function(e, xhr, opts, err){
      console.log("testError")
      $('#result').html('Error: ' + err);
    })
    //.fail(function() {
    //  $('#result').html('Failed.');
    //})
    //$(document)
    //.ajaxStop(function(){
    //  $('#prog').hide();
    //})
  });
  return false;
});
