var CurrentBooked = {};


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


function update_visual_status(row, seat, status) {
    var status_map = {
        '0': 'free',
        '1': 'tentative-booked',
        '2': 'booked'
    };
    var target = $('.row .' + row + '_' + seat);
    target.removeClass('free tentative booked');
    target.addClass(status_map[status]);
}


function get_reservations() {
    // Load reservations after selecting a movie.
    CurrentBooked['movie'] = $('.movie-chooser').val();
    $.get('/api/movies/' + CurrentBooked['movie'] + '/reservation_list/', {}, function(data) {
        // iterate over the seats and update their statuses
        // (selected by others are unclickable!)
        $('.step_2').hide();
        $.each(data, function(index, reservation) {
                update_visual_status(reservation['seat']['row']['name'], reservation['seat']['number'], reservation['status'] );
            }
        );
        $('.step_3').show();
    });
}


function step_forward() {

}

function book() {
    // book a seat

}


$(document).ready(function() {
    get_movies();
    $('.step_2_next').click(function() {
        get_reservations();
    });

    $('.row .seat').click(function() {
        var id = $(this).attr('id').split('_');
        var row = id[0];
        var seat = id[1];
        // run checks against matching row, max number of seats, adjacency etc. etc. etc.
        $(this).toggleClass('selected');
        if (typeof CurrentBooked['row'] == 'undefined') {
            CurrentBooked['row'] = row;
        }
        if (typeof CurrentBooked['seats'] == 'undefined') {
            CurrentBooked['seats'] = [];
        }
        CurrentBooked['seats'].push(seat);
    });


});