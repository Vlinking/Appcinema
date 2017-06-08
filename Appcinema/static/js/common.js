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


function update_visual_status(seat, status) {
    var status_map = {
        '0': 'free',
        '1': 'tentative-booked',
        '2': 'booked'
    };
    var target = $('#seat_' + seat);
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
                update_visual_status(reservation['seat'].id, reservation['status'] );
            }
        );
        $('.step_3').show();
    });
}


function step_forward() {
    $('.step_3').hide();
   var container = $('.confirmation-info');
   var child = $("<div>");
   child.html('Row: ' + CurrentBooked['row']);
   container.append(child);
   $.each(CurrentBooked['seats'], function(index, object) {
        var child = $("<div>");
        child.html('Seat ' + object);
        container.append(child);
   });
    $('.step_4').show();
}

function confirm() {
       var data = $('.confirmation').serialize();
       data = data + '&row=' + CurrentBooked['row'] + '&seats=' + CurrentBooked['seats'].join() + '&movie=' + CurrentBooked['movie'];
       $.post('/api/confirm_reservation/', data, function(result) {
            $('.step_4').hide();
            $('.step_5').show();
       });
}

function book(seat, movie) {
    // book a seat
       var data = $('.seats').serialize();
       data = data + '&seat=' + seat + '&movie=' + movie + '&status=1';
       $.post('/api/reservation/', data, function(result) {
           $('#seat_' + seat).addClass('selected');
       });
}

function unbook(seat, movie) {
    // unbook a seat
       var data = $('.seats').serialize();
       data = data + '&seat=' + seat + '&movie=' + movie + '&status=0';
       $.post('/api/reservation/', data, function(result) {
           $('#seat_' + seat).removeClass('selected');
       });
}

$(document).ready(function() {
    get_movies();
    $('.step_2_next').click(function() {
        get_reservations();
    });

    $('.row .seat').click(function() {
        // selected by others are unclickable
        if (($(this).hasClass('tentative-booked')) || ($(this).hasClass('booked'))) {
            return;
        }
        var id = $(this).attr('id').split('_');
        var seat = id[1];
        // todo run checks against matching row, max number of seats, adjacency etc. etc. etc.
        if (typeof CurrentBooked['row'] == 'undefined') {
            // todo temporary
            CurrentBooked['row'] = '';
        }
        if (typeof CurrentBooked['seats'] == 'undefined') {
            CurrentBooked['seats'] = [];
        }
        if (!$(this).hasClass('selected')) {
            book(seat, CurrentBooked['movie']);
            CurrentBooked['seats'].push(seat);
        } else {
            unbook(seat, CurrentBooked['movie']);
            CurrentBooked['seats'].splice( $.inArray(seats, CurrentBooked['seats']), 1 );
        }
    });

    $('.step_3_next').click(function() {
        step_forward();
    });

    $('.step_4_confirm').click(function() {
        confirm();
    });

});