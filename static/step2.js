$(document).ready(function () {

    $.ajax({
        type: "GET",
        url: "https://" + window.location.hostname + "/radiorecsservices/music_genres",

        success: function (musicGenres) {
            const musicGenresParsed = JSON.parse(musicGenres)
            populateMusicGenresList(musicGenresParsed)
        },
        error: function (request) {
            const errorMessage = request.responseText.trim()
            alert(errorMessage)
        }
    });
});

function populateMusicGenresList(musicGenres) {
    musicGenres.forEach(musicGenre => {
        $('<option />', {
            text: musicGenre,
            id: musicGenre
        })
        .appendTo("#musicGenres");
    })
}
