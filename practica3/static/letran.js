$(document).ready(function(){
var tamOriginal = $('div').css('font-size');
$(".reiFuente").click(function(){
$('div').css('font-size', tamOriginal);
});

$(".aumFuente").click(function(){
var tamActual = $('div').css('font-size');
var tamActualNum = parseFloat(tamActual, 10);
var nuevaFuente = tamActualNum*1.2;
$('div').css('font-size', nuevaFuente);
return false;
});

$(".disFuente").click(function(){
var tamActual = $('div').css('font-size');
var tamActualNum = parseFloat(tamActual, 10);
var nuevaFuente = tamActualNum*0.8;
$('div').css('font-size', nuevaFuente);
return false;
});
});


$(document).ready(function(){
    $("button").click(function(){
        $(".aumFuente").fadeToggle();
        $(".disFuente").fadeToggle("slow");
        $(".reiFuente").fadeToggle(3000);
    });
});


