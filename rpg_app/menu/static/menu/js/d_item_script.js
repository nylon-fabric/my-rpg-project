document.addEventListener('DOMContentLoaded', function() {
  var img = document.getElementById('img');

  var goImg = new Array('../../static/menu/js/media/main.png', 
                         '../../static/menu/js/media/go1.png', 
                         '../../static/menu/js/media/go2.png', 
                         '../../static/menu/js/media/go3.png', 
                         '../../static/menu/js/media/go4.png', 
                         '../../static/menu/js/media/go5.png', 
                         '../../static/menu/js/media/go6.png'
                        );

var bentImg = new Array('../../static/menu/js/media/main.png', 
                         '../../static/menu/js/media/bent1.png', 
                         '../../static/menu/js/media/bent2.png', 
                         '../../static/menu/js/media/bent3.png', 
                         '../../static/menu/js/media/bent4.png', 
                         '../../static/menu/js/media/bent5.png'
                        );

  var speed1 = 150;
  var speed2 = 300;
  var speed3 = 450;
  var speed4 = 600;
  var speed5 = 750;
  var speed6 = 900;

  document.getElementById('left').addEventListener('click', function(){
       img.src = bentImg[1]
    setTimeout(function(){img.src = bentImg[2]}, speed1);
    setTimeout(function(){img.src = bentImg[3]}, speed2);
    setTimeout(function(){img.src = bentImg[4]}, speed3);
    setTimeout(function(){img.src = bentImg[5]}, speed4);
    setTimeout(function(){img.src = bentImg[0]}, speed5);
  }, false);
 
  document.getElementById('right').addEventListener('click', function(){
    img.src = bentImg[5]
    setTimeout(function(){img.src = bentImg[4]}, speed1);
    setTimeout(function(){img.src = bentImg[3]}, speed2);
    setTimeout(function(){img.src = bentImg[2]}, speed3);
    setTimeout(function(){img.src = bentImg[1]}, speed4);
    setTimeout(function(){img.src = bentImg[0]}, speed5);
  }, false);

  img.src = goImg[0];

},false);