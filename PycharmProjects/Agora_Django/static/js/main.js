/**
 * Created by sam on 25/08/14.
 */

$(document).ready(function(){

          $('#username').bind('mouseover', openMenu);
          $('nav').bind('mouseover', openMenu);
          $('nav').bind('mouseout', closeMenu);

            function openMenu(){
              $('nav').css('visibility', 'visible');
            };

            function closeMenu(){
              $('nav').css('visibility', 'hidden');
            };

    $('#iconShare').click(function(){
        if($('#linkpop').css('visibility')=="visible"){
            $('#linkpop').css('visibility','hidden');
        }else{
            $('#linkpop').css('visibility','visible');
        }
    })

});
