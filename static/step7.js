$(document).ready(function () {

    // Call RS1a
    $.ajax({
        type: "GET",
        url: "http://localhost:9090/rs1a?voice=" + voicePercentage + "&music=" + (100 - voicePercentage),

        success: function (result) {
            const resultParsed = JSON.parse(result)
            processResult(resultParsed)
        },
        error: function () {
            alert('fail')
        }
    });

    // Call RS2a
    let musicGenresArguments = ""
    let musicGenresString = musicGenres.toString()
    let musicGenresList = musicGenresString.split(",")
    for (let musicGenreIndex in musicGenresList) {
        let musicGenre = musicGenresList[musicGenreIndex]
        musicGenresArguments += musicGenre + "=1&"
    }
    if (musicGenresArguments.length !== 0) {
        musicGenresArguments = musicGenresArguments.slice(0, -1)
    }

    $.ajax({
        type: "GET",
        url: "http://localhost:9090/rs2a?" + musicGenresArguments,

        success: function (result) {
            const resultParsed = JSON.parse(result)
            processResult(resultParsed)
        },
        error: function () {
            alert('fail')
        }
    });

    // Call RS3a
    let topicsArguments = ""
    let topicsString = topics.toString()
    let topicsList = topicsString.split(",")

    if (topicsList.includes("informativo")) {
        topicsArguments += "news=1&"
    } else {
        topicsArguments += "news=0&"
    }
    if (topicsList.includes("deportes")) {
        topicsArguments += "sport=1&"
    } else {
        topicsArguments += "sport=0&"
    }
    if (topicsList.includes("entretenimiento")) {
        topicsArguments += "entertainment=1&"
    } else {
        topicsArguments += "entertainment=0&"
    }
    if (topicsList.includes("musical")) {
        topicsArguments += "musical=1&"
    } else {
        topicsArguments += "musical=0&"
    }
    if (topicsList.includes("educacion")) {
        topicsArguments += "education=1"
    } else {
        topicsArguments += "education=0"
    }

    $.ajax({
        type: "GET",
        url: "http://localhost:9090/rs3a?" + topicsArguments,

        success: function (result) {
            const resultParsed = JSON.parse(result)
            processResult(resultParsed)
        },
        error: function () {
            alert('fail')
        }
    });

    // Call RS4a
    let toneArguments = ""

    toneArguments += "analytical=" + (analyticalPercentage / 100) + "&"
    toneArguments += "anger=" + (angerPercentage / 100) + "&"
    toneArguments += "confident=" + (confidentPercentage / 100) + "&"
    toneArguments += "fear=" + (fearPercentage / 100) + "&"
    toneArguments += "joy=" + (joyPercentage / 100) + "&"
    toneArguments += "sadness=" + (sadnessPercentage / 100) + "&"
    toneArguments += "tentative=" + (tentativePercentage / 100)

    console.log("tonesArguments: " + toneArguments)

    $.ajax({
        type: "GET",
        url: "http://localhost:9090/rs4a?" + toneArguments,

        success: function (result) {
            const resultParsed = JSON.parse(result)
            processResult(resultParsed)
        },
        error: function () {
            alert('fail')
        }
    });
});

function processResult(result) {
    console.log(result)
}
