$(document).ready(function(){
    var class_toggle = '<a class="toggle" href="#"><img title="Hide Class Details" src="_static/minus.png" alt="-"/></a>';
    $("dl.class").prepend(class_toggle);
    $("dl.interface").prepend(class_toggle);

    $(".toggle").click(function(event) {
    	var img = $(this).children('img');
    	
    	if (img.attr('alt') == '-') {
    		img.attr('title', 'Show Details');
    		img.attr('src', '_static/plus.png');
    		img.attr('alt', '+');
    		
    		$(this).parent().children('dd').css('display', 'none');
    	}
    	else {
    		img.attr('title', 'Hide Details');
    		img.attr('src', '_static/minus.png');
    		img.attr('alt', '-');
    		
    		$(this).parent().children('dd').css('display', 'block');
    	}
        return false;
    });
});

