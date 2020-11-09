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
        programs: programs
    });

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
        error: function (errorMessage) {
            alert(errorMessage)
            stopProcessing()
        }
    });
}

function populatePredictionList(prediction) {
    prediction.forEach(program => {
        $('<li class="list-group-item">' + program + '</li>').appendTo("#prediction")
    })
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
