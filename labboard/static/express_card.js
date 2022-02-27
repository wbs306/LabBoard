$(".track:last-child .timeline").remove();
$(".track:first-child p").removeClass("text-muted");
$(".track-detail:first-child").addClass("active");
$(".package-item:first-child").addClass("active");

let input_timer;
let last_input;
$("#add-package input").on("keyup", e => {
    clearTimeout(input_timer);
    input_timer = setTimeout(() => {
        let curr_input = $("#add-package input").val();
        if (last_input == curr_input)
            return;
        last_input = curr_input;
        let spinner = $("<div class='spinner-border text-primary' role='status'><span class='visually-hidden'>Loading...</span></div>");
        $("#add-package p").remove();
        $("#add-package .spinner-border").remove();
        $("#add-package").append(spinner);
        $.post($SCRIPT_ROOT + "/express/getExpressCompany", {
            "number": curr_input
        }, (data) => {
            spinner.remove();
            let company = $("<p></P>");
            if (data["company"]) {
                company.attr("id", "company-" + data["company"]);
                $("#add-package button").removeClass("disabled");
            }                
            company.text(data["name"]);
            $("#add-package").append(company);
        });
    }, 2000)
})

function addPackage() {
    let number = $("#add-package input").val();
    let company = $("#add-package p").attr("id").split("-")[1];
    $.post($SCRIPT_ROOT + "/express/addPackage", {
        "number": number,
        "company": company,
        "name": $("#add-package p").text()
    }, (data) => {
        if (data["state"] != "ok")
            return;
    });

    $.post($SCRIPT_ROOT + "/express/getExpressState", {
        "number": number,
        "company": company
    }, (data) => {
        let result = $(data);
        $("#packages-list").append(result[0]);
        $("#express-card .col-7 .tab-content").append(result[2]);
    });
}

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