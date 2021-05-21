$(document).ready(function() {

    $("#useCustomWeights").change(function() {
        const customWeights = $("#customWeights")
        if (this.checked) {
            customWeights.css("pointer-events", "all")
            customWeights.css("opacity", "1.0")
        } else {
            customWeights.css("pointer-events", "none")
            customWeights.css("opacity", "0.4")
        }
    })
})
