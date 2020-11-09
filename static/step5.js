$(document).ready(function () {

    // Get providers and algorithms
    $.ajax({
        type: "GET",
        url: "http://" + window.location.hostname + ":9090/programs",

        success: function (programs) {
            const programsParsed = JSON.parse(programs)
            populateProgramsList(programsParsed)
        },
        error: function () {
            alert('fail');
        }
    });
});

function populateProgramsList(programs) {
    programs.forEach(program => {
        $('<option />', {
            text: program,
            id: program
        })
        .appendTo("#programs");
    })
}
