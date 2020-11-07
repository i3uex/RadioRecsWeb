$(document).ready(function () {

    // Get providers and algorithms
    $.ajax({
        type: "GET",
        url: "http://localhost:9090/topics",

        success: function (topics) {
            const topicsParsed = JSON.parse(topics)
            populateTopicsList(topicsParsed)
        },
        error: function () {
            alert('fail');
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
