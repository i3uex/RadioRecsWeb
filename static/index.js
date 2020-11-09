const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
const feedback = urlParams.get("feedback")

$(document).ready(function () {
    console.log("feedback: " + feedback)
    if (feedback) {
        saveFeedback()
    }
});

function saveFeedback() {
    let data = JSON.stringify({
        feedback: feedback
    });

    $.ajax({
        type: "POST",
        data: {data},
        url: "/save_feedback",

        success: function () {
            console.log("Feedback saved successfully")
        },
        error: function (errorMessage) {
            console.log("Error saving feedback")
            console.log(errorMessage)
        }
    });
}
