$(".track:last-child .timeline").remove();
$(".track:first-child p").removeClass("text-muted");
$(".track-detail:first-child").addClass("active");
$(".package-item:first-child").addClass("active");

function deletePackage() {
    let curr_item = $(".package-item.active");
    let curr_track = $(".track-detail.active");
    if ($(".package-item").length > 1) {
        curr_item.next().addClass("active");
        curr_track.next().addClass("active");
    }

    curr_item.remove();
    curr_track.remove();

    $.post($SCRIPT_ROOT + "/express/deletePackage", {
        "number": curr_item.attr("href").split("-")[1],
        "name": curr_item.find("h5").text(),
    });
}