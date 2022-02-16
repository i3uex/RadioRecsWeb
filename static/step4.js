$(document).ready(function () {

    // Get providers and algorithms
    $.ajax({
        type: "GET",
        url: "https://" + window.location.hostname + "/radiorecsservices/topics",

        success: function (topics) {
            const topicsParsed = JSON.parse(topics)
            populateTopicsList(topicsParsed)
        },
        error: function (request) {
            const errorMessage = request.responseText.trim()
            alert(errorMessage)
        }
    });
});

function populateTopicsList(topics) {
    topics.forEach(topic => {
        $('<option />', {
            text: topic,
            id: topic
        })
        .appendTo("#topics");
    })
}
