$(document).ready(function () {
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
        programs: programs,
        voiceMusicWeight: voiceMusicWeight,
        genresWeight: genresWeight,
        topicsWeight: topicsWeight,
        tonesWeight: tonesWeight
    });

    console.log(data)

    $('#restart_button').html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Processing...').addClass('disabled')
    $("#patient_warning").show()

    $.ajax({
        type: "POST",
        data: {data},
        url: "/make_prediction",

        success: function (prediction) {
            const predictionParsed = JSON.parse(prediction)
            populatePredictionList(predictionParsed)
            stopProcessing()
        },
        error: function (request) {
            const errorMessage = request.responseText.trim()
            alert(errorMessage)
            stopProcessing()
        }
    });
}

function populatePredictionList(prediction) {
    console.log(prediction)
    for (let program_name in prediction) {
        if (prediction.hasOwnProperty(program_name)) {
            let program_weight = prediction[program_name]
            $('<li class="list-group-item">' + program_name + ' <sub>' + program_weight + '</sub></li>').appendTo("#prediction")
        }
    }
}

function stopProcessing() {
    $('#restart_button').html("Submit and Restart")
    $("#restart_button").removeClass("disabled")
    $("#patient_warning").hide()
    $("#feedback").show()
}

function restart() {
    $("#form").submit()
}
