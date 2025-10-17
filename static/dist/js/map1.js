

var legend = 'on'
$("#legBox").on('click', function() {
    if (legend == 'on') {
        $("#lgd").slideUp("slow");
        legend = 'off';
    } else if (legend == 'off') {
        $("#bsmp").slideUp("fast");
        $("#lgd").slideDown("slow");
        basemap = 'off';
        legend = 'on';
    }
});


var basemap = 'off'
$("#baseMap").on('click', function() {
    if (basemap == 'on') {
        $("#bsmp").slideUp("slow");
        basemap = 'off';
    } else if (basemap == 'off') {
        $("#lgd").slideUp("fast");
        $("#bsmp").slideDown("slow");
        legend = 'off';
        basemap = 'on';
    }
});