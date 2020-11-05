const musicUrl = "/static/step2.html"
const toneUrl = "/static/step3.html"
const topicsUrl = "/static/step4.html"
const summaryUrl = "/static/step5.html"

const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)

const voicePercentage = urlParams.get("voicePercentage")
const musicGenres = urlParams.getAll("musicGenres")
const analyticalPercentage = urlParams.get("analyticalPercentage")
const angerPercentage = urlParams.get("angerPercentage")
const confidentPercentage = urlParams.get("confidentPercentage")
const fearPercentage = urlParams.get("fearPercentage")
const joyPercentage = urlParams.get("joyPercentage")
const sadnessPercentage = urlParams.get("sadnessPercentage")
const tentativePercentage = urlParams.get("tentativePercentage")
const topics = urlParams.getAll("topics")

$(document).ready(function() {
    const musicPercentageItem = $("#musicPercentage")
    const voicePercentageItem = $("#voicePercentage")
    const musicGenresItem = $("#musicGenres")
    const analyticalPercentageItem = $("#analyticalPercentage")
    const angerPercentageItem = $("#angerPercentage")
    const confidentPercentageItem = $("#confidentPercentage")
    const fearPercentageItem = $("#fearPercentage")
    const joyPercentageItem = $("#joyPercentage")
    const sadnessPercentageItem = $("#sadnessPercentage")
    const tentativePercentageItem = $("#tentativePercentage")
    const topicsItem = $("#topics")

    voicePercentageItem.val(voicePercentage)
    musicGenresItem.val(musicGenres)
    analyticalPercentageItem.val(analyticalPercentage)
    angerPercentageItem.val(angerPercentage)
    confidentPercentageItem.val(confidentPercentage)
    fearPercentageItem.val(fearPercentage)
    joyPercentageItem.val(joyPercentage)
    sadnessPercentageItem.val(sadnessPercentage)
    tentativePercentageItem.val(tentativePercentage)
    topicsItem.val(topics)

    if (window.location.pathname === "/static/step3.html" && voicePercentage > 50) {
        $("#form").attr("action", musicUrl)
    }

    if (window.location.pathname === "/static/step2.html" && voicePercentage > 50) {
        $("#form").attr("action", summaryUrl)
    }


    if (window.location.pathname === "/static/step5.html") {
        musicPercentageItem.text((100 - voicePercentage) + "%")
        voicePercentageItem.text(voicePercentage + "%")
        musicGenresItem.text(musicGenres)
        analyticalPercentageItem.text(analyticalPercentage + "%")
        angerPercentageItem.text(angerPercentage + "%")
        confidentPercentageItem.text(confidentPercentage + "%")
        fearPercentageItem.text(fearPercentage + "%")
        joyPercentageItem.text(joyPercentage + "%")
        sadnessPercentageItem.text(sadnessPercentage + "%")
        tentativePercentageItem.text(tentativePercentage + "%")
        topicsItem.text(topics)
    }
})

function updateMusicVoicePercentage() {
    const voicePercentage = $("#voicePercentage").val()

    const text = "Music (" + (100 - voicePercentage) + "%) | Voice (" + voicePercentage + "%)"
    $("#voicePercentageLabel").text(text)
    if (voicePercentage <= 50) {
        $("#form").attr("action", musicUrl)
    } else {
        $("#form").attr("action", toneUrl)
    }
}

function updateRange(rangeInput, rangeInputLabel, prefix) {
    const value = $("#" + rangeInput).val()
    const text = prefix + " (" + value + "%)"
    $("#" + rangeInputLabel).text(text)
    if (value <= 50) {
        $("#button").attr("href", musicUrl)
    } else {
        $("#button").attr("href", toneUrl)
    }
}
