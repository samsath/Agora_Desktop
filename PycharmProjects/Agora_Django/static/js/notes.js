
$(document).ready(function(){

    function noteClick(number){
        console.log(notelist[number].name);

    };

    var wall = new freewall("#firewall");

    wall.reset({
        selector: '.brick',
        animate: true,
        cellW: 160,
        cellH: 160,
        delay: 50,
        onResize: function(){
            wall.fitWidth();
        }
    });
    wall.fitWidth();

    var temp = '<div class="brick {size} .note" style="background-color:{bgcolour};width:200px;height:200px;margin:10px;"><a href="{name}" style="text-decoration: none; color:{txcolour};"><p maxlength="200">{content}</p></a></div>';
    var size = "size33 size32 size31 size23 size22 size21 size13 size12 size11".split(" ");

    for(var n =0; n<notelist.length;n++){
        var html ="";

        html += temp
            .replace('{size}', size[size.length * Math.random() << 0])
            .replace('{bgcolour}',notelist[n].bg)
            .replace('{txcolour}',notelist[n].tx)
            .replace('{name}',notelist[n].name)
            .replace('{content}',notelist[n].content.slice(0,176));



        wall.prepend(html);
    }





});

