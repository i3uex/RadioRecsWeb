let rs1aResult = ""
let rs2aResult = ""
let rs3aResult = ""
let rs4aResult = ""

$(document).ready(function () {
    rs1a()
});

function rs1a() {
    $.ajax({
        type: "GET",
        url: "http://localhost:9090/rs1a?voice=" + voicePercentage + "&music=" + (100 - voicePercentage),

        success: function (result) {
            console.log(result)
            rs1aResult = JSON.parse(result)
            rs2a()
        },
        error: function () {
            alert('fail')
        }
    });
}

function rs2a() {
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
            rs2aResult = JSON.parse(result)
            rs3a()
        },
        error: function () {
            alert('fail')
        }
    });
}

function rs3a() {
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
            rs3aResult = JSON.parse(result)
            rs4a()
        },
        error: function () {
            alert('fail')
        }
    });
}

function rs4a() {
    let toneArguments = ""

    toneArguments += "analytical=" + (analyticalPercentage / 100) + "&"
    toneArguments += "anger=" + (angerPercentage / 100) + "&"
    toneArguments += "confident=" + (confidentPercentage / 100) + "&"
    toneArguments += "fear=" + (fearPercentage / 100) + "&"
    toneArguments += "joy=" + (joyPercentage / 100) + "&"
    toneArguments += "sadness=" + (sadnessPercentage / 100) + "&"
    toneArguments += "tentative=" + (tentativePercentage / 100)

    $.ajax({
        type: "GET",
        url: "http://localhost:9090/rs4a?" + toneArguments,

        success: function (result) {
            rs1aResult = JSON.parse(result)
            makePrediction()
        },
        error: function () {
            alert('fail')
        }
    });
}

function makePrediction() {
    console.log("rs1aResult: " + rs1aResult)
    console.log("rs2aResult: " + rs2aResult)
    console.log("rs3aResult: " + rs3aResult)
    console.log("rs4aResult: " + rs4aResult)
}
