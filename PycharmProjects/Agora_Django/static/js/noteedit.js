$(document).ready(function(){

    var bg = document.getElementById('id_noteForm-0-bg_colour').value;
    var tx= document.getElementById('id_noteForm-0-tx_colour').value;


    $('#id_noteForm-0-content').css('background-color',bg)
                           .css('color',tx)
                           .css('font-size','xx-large')
                           .attr('readonly','readonly');


  $('#editButton').click(function(){
    $('#notespec').css('visibility','visible');
    $(this).css('visibility','hidden');
    $('#id_noteForm-0-content').attr('readonly',false);
  });

  $('#archiveButton').click(function(){
      if($('#archive').css('visibility')=='hidden'){
         $('#archive').css('visibility',"visible");
      }else{
          $('#archive').css('visibility',"hidden");
      }
  });

  $('#bgChange').click(function(){
      if ($('#colourPalete').css('visibility')=='visible'&& $('#CPvalue').text()=="bg"){
          $('#colourPalete').css('visibility','hidden');
          $('#CPvalue').text("");
      }else{
          $('#colourPalete').css('visibility','visible');
          $('#CPvalue').text("bg");
      }
  });

  $('#txChange').click(function(){
      if ($('#colourPalete').css('visibility')=='visible' && $('#CPvalue').text()=="tx"){
          $('#colourPalete').css('visibility','hidden');
          $('#CPvalue').text("");
      }else{
          $('#colourPalete').css('visibility','visible');
          $('#CPvalue').text("tx");
      }
  });

  $('#ff6600').click(function(){
      if($('#CPvalue').text()=="tx"){
          document.getElementById('id_noteForm-0-tx_colour').value = "#ff6600";
          $('#id_noteForm-0-content').css('color',"#ff6600");
      }else{
          document.getElementById('id_noteForm-0-bg_colour').value = "#ff6600";
          $('#id_noteForm-0-content').css('background-color',"#ff6600");
      }
  });

  $('#2d2d2d').click(function(){
      if($('#CPvalue').text()=="tx"){
          document.getElementById('id_noteForm-0-tx_colour').value = "#2d2d2d";
          $('#id_noteForm-0-content').css('color',"#2d2d2d");
      }else{
          document.getElementById('id_noteForm-0-bg_colour').value = "#2d2d2d";
          $('#id_noteForm-0-content').css('background-color',"#2d2d2d");
      }
  });

  $('#104ba9').click(function(){
      if($('#CPvalue').text()=="tx"){
          document.getElementById('id_noteForm-0-tx_colour').value = "#104ba9";
          $('#id_noteForm-0-content').css('color',"#104ba9");
      }else{
          document.getElementById('id_noteForm-0-bg_colour').value = "#104ba9";
          $('#id_noteForm-0-content').css('background-color',"#104ba9");
      }
  });

  $('#1db312').click(function(){
      if($('#CPvalue').text()=="tx"){
          document.getElementById('id_noteForm-0-tx_colour').value = "#1db312";
          $('#id_noteForm-0-content').css('color',"#1db312");
      }else{
          document.getElementById('id_noteForm-0-bg_colour').value = "#1db312";
          $('#id_noteForm-0-content').css('background-color',"#1db312");
      }
  });

  $('#e0e0e0').click(function(){
      if($('#CPvalue').text()=="tx"){
          document.getElementById('id_noteForm-0-tx_colour').value = "#e0e0e0";
          $('#id_noteForm-0-content').css('color',"#e0e0e0");
      }else{
          document.getElementById('id_noteForm-0-bg_colour').value = "#e0e0e0";
          $('#id_noteForm-0-content').css('background-color',"#e0e0e0");
      }
  });

  $('#ff270d').click(function(){
      if($('#CPvalue').text()=="tx"){
          document.getElementById('id_noteForm-0-tx_colour').value = "#ff270d";
          $('#id_noteForm-0-content').css('color',"#ff270d");
      }else{
          document.getElementById('id_noteForm-0-bg_colour').value = "#ff270d";
          $('#id_noteForm-0-content').css('background-color',"#ff270d");
      }
  });

  $('#51dee0').click(function(){
      if($('#CPvalue').text()=="tx"){
          document.getElementById('id_noteForm-0-tx_colour').value = "#51dee0";
          $('#id_noteForm-0-content').css('color',"#51dee0");
      }else{
          document.getElementById('id_noteForm-0-bg_colour').value = "#51dee0";
          $('#id_noteForm-0-content').css('background-color',"#51dee0");
      }
  });

  $('#ffcb25').click(function(){
      if($('#CPvalue').text()=="tx"){
          document.getElementById('id_noteForm-0-tx_colour').value = "#ffcb25";
          $('#id_noteForm-0-content').css('color',"#ffcb25");
      }else{
          document.getElementById('id_noteForm-0-bg_colour').value = "#ffcb25";
          $('#id_noteForm-0-content').css('background-color',"#ffcb25");
      }
  });

  $('#834c24').click(function(){
      if($('#CPvalue').text()=="tx"){
          document.getElementById('id_noteForm-0-tx_colour').value = "#834c24";
          $('#id_noteForm-0-content').css('color',"#834c24");
      }else{
          document.getElementById('id_noteForm-0-bg_colour').value = "#834c24";
          $('#id_noteForm-0-content').css('background-color',"#834c24");
      }
  });

  $('#00ff00').click(function(){
      if($('#CPvalue').text()=="tx"){
          document.getElementById('id_noteForm-0-tx_colour').value = "#00ff00";
          $('#id_noteForm-0-content').css('color',"#00ff00");
      }else{
          document.getElementById('id_noteForm-0-bg_colour').value = "#00ff00";
          $('#id_noteForm-0-content').css('background-color',"#00ff00");
      }
  });


});