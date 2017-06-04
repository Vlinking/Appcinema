
function get_movies() {
    // Load movie data into a select element.
    $.get('/api/movies', {}, function(data) {
           var container = $('.movie-chooser');
           $.each(data, function(index, object) {
                child = $("<option>", {value: object.id});
                child.html(object.title);
                container.append(child);
           });
       });
}

function get_reservations() {
    // Load reservations after selecting a movie.
    $.get('/api/movies/' + $('.movie-chooser').val() + '/reservation_list/', {}, function(data) {
        // iterate over the seats and update their statuses
        // (selected by others are unclickable!)
        $('.step_2').hide();
        $.each(data, function(index, seat) {
                console.log(seat);
            }
        );
        $('step_3').show();
    });
}



$(document).ready(function() {
    get_movies();
    $('.step_2_next').click(function() {
        get_reservations();
    });

});