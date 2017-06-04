
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

$(document).ready(function() {
    get_movies();

});