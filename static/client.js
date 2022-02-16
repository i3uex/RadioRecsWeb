const musicUrl = "step2.html"
const toneUrl = "step3.html"
const topicsUrl = "step4.html"
const summaryUrl = "step6.html"

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
const programs = urlParams.getAll("programs")
const voiceMusicWeight = urlParams.get("voiceMusicWeight")
const genresWeight = urlParams.get("genresWeight")
const topicsWeight = urlParams.get("topicsWeight")
const tonesWeight = urlParams.get("tonesWeight")

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
    const programsItem = $("#programs")
    const voiceMusicWeightItem = $("#voiceMusicWeight")
    const genresWeightItem = $("#genresWeight")
    const topicsWeightItem = $("#topicsWeight")
    const tonesWeightItem = $("#tonesWeight")

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
    programsItem.val(programs)
    voiceMusicWeightItem.val(voiceMusicWeight)
    genresWeightItem.val(genresWeight)
    topicsWeightItem.val(topicsWeight)
    tonesWeightItem.val(tonesWeight)

    let path = window.location.pathname
    let pathSegments = path.split("/")
    let pathLastSegment = pathSegments.pop()

    if (pathLastSegment === toneUrl && voicePercentage > 50) {
        $("#form").attr("action", musicUrl)
    }

    if (pathLastSegment === musicUrl && voicePercentage > 50) {
        $("#form").attr("action", topicsUrl)
    }

    if (pathLastSegment === summaryUrl) {
        const musicPercentageDisplayItem = $("#musicPercentageDisplay")
        const voicePercentageDisplayItem = $("#voicePercentageDisplay")
        const musicGenresDisplayItem = $("#musicGenresDisplay")
        const analyticalPercentageDisplayItem = $("#analyticalPercentageDisplay")
        const angerPercentageDisplayItem = $("#angerPercentageDisplay")
        const confidentPercentageDisplayItem = $("#confidentPercentageDisplay")
        const fearPercentageDisplayItem = $("#fearPercentageDisplay")
        const joyPercentageDisplayItem = $("#joyPercentageDisplay")
        const sadnessPercentageDisplayItem = $("#sadnessPercentageDisplay")
        const tentativePercentageDisplayItem = $("#tentativePercentageDisplay")
        const topicsDisplayItem = $("#topicsDisplay")
        const programsDisplayItem = $("#programsDisplay")

        musicPercentageDisplayItem.text((100 - voicePercentage) + "%")
        voicePercentageDisplayItem.text(voicePercentage + "%")
        musicGenresDisplayItem.text(musicGenres)
        analyticalPercentageDisplayItem.text(analyticalPercentage + "%")
        angerPercentageDisplayItem.text(angerPercentage + "%")
        confidentPercentageDisplayItem.text(confidentPercentage + "%")
        fearPercentageDisplayItem.text(fearPercentage + "%")
        joyPercentageDisplayItem.text(joyPercentage + "%")
        sadnessPercentageDisplayItem.text(sadnessPercentage + "%")
        tentativePercentageDisplayItem.text(tentativePercentage + "%")
        topicsDisplayItem.text(topics)
        programsDisplayItem.text(programs)
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
