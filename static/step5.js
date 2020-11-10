$(document).ready(function () {

    // Get providers and algorithms
    $.ajax({
        type: "GET",
        url: "http://" + window.location.hostname + ":9090/program_names",

        success: function (programs) {
            const programsParsed = JSON.parse(programs)
            populateProgramsList(programsParsed)
        },
        error: function (request) {
            const errorMessage = request.responseText.trim()
            alert(errorMessage)
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
