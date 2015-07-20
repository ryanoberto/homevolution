$(document).ready(function () {
    $.simpleWeather({
        location: 'Johannesburg, SA',
        woeid: '',
        unit: 'c',
        success: function (weather) {
            html = '<h2><i class="icon-' + weather.code + '"></i> ' + weather.temp + '&deg;' + weather.units.temp + '</h2>';
            //html += '<ul><li>' + weather.city + ', ' + weather.region + '</li>';
            html += weather.currently + '<br>';
            $('#weather').html(html);
        },
        error: function (error) {
            $('#weather').html('<p>' + error + '</p>');
        }
    });
});
