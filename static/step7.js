let rs1aResult = ""
let rs2aResult = ""
let rs3aResult = ""
let rs4aResult = ""

$(document).ready(function () {
    // rs1a()
    makePrediction()
});

function makePrediction() {
    let data = JSON.stringify({
        voicePercentage: voicePercentage,
        musicGenres: musicGenres,
        analyticalPercentage: analyticalPercentage,
        angerPercentage: angerPercentage,
        confidentPercentage: confidentPercentage,
        fearPercentage: fearPercentage,
        joyPercentage: joyPercentage,
        sadnessPercentage: sadnessPercentage,
        tentativePercentage: tentativePercentage,
        topics: topics,
        programs: programs
    });

    $.ajax({
        type: "POST",
        data: {data},
        url: "/make_prediction",

        success: function (result) {
            console.log(result)
        },
        error: function () {
            alert('fail');
        }
    });
}
