const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
const feedback = urlParams.get("feedback")
const position = urlParams.get("position")
const will_listen = urlParams.get("will_listen")

$(document).ready(function () {
    console.log("feedback: " + feedback)
    if (feedback) {
        saveFeedback()
    }
});

function saveFeedback() {
    let data = JSON.stringify({
        feedback: feedback,
        position: position,
        will_listen: will_listen
    });

    $.ajax({
        type: "POST",
        data: {data},
        url: "/save_feedback",

        success: function () {
            console.log("Feedback saved successfully")
        },
        error: function (request) {
            const errorMessage = request.responseText.trim()
            alert(errorMessage)
        }
    });
}
