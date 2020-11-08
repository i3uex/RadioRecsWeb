$(document).ready(function () {

    $.ajax({
        type: "GET",
        url: "http://localhost:9090/music_genres",

        success: function (musicGenres) {
            const musicGenresParsed = JSON.parse(musicGenres)
            populateMusicGenresList(musicGenresParsed)
        },
        error: function () {
            alert('fail');
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
