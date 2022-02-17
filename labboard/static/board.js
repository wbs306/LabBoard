var week = {
  0: "周日", 1: "周一", 2: "周二", 3: "周三",
  4: "周四", 5: "周五", 6: "周六"
};

function clock() {
  let date = new Date();
  let hour = date.getHours().toString();
  let minutes = date.getMinutes().toString();
  if (hour.length == 1)
      hour = "0" + hour;
  if (minutes.length == 1)
      minutes = "0" + minutes;
  $("#time").text(hour + ":" + minutes);
  $("#week").text((date.getMonth() + 1) + "月" + date.getDate() + "日    " + week[date.getDay()]);
}

function getLocationData() {
  let location_name = $("input[name=location]").val();
  $("#location-modal .alert").remove();
  $("#location-modal .spinner-border").remove();
  if (location_name == "") {
    $("#location-modal .modal-body").append($("<div class='alert alert-danger' role='alert'>请输入城市名字</div>"));
    return;
  }
  let select = $("<select class='form-select' name='city-select'>");
  let spinner = $("<div class='spinner-border text-primary' role='status'><span class='visually-hidden'>Loading...</span></div>");
  $("#location-modal .modal-body").append(spinner);
  $.post($SCRIPT_ROOT + "/weather/getLocation", {
    "location": location_name
  }, function (data) {
    $("#location-modal select").remove();
    spinner.remove();
    for (let city of data) {
      let new_option = $("<option></option>");
      new_option.text(city["country"] + ", " + city["adm1"] + ", " + city["adm2"] + ", " + city["name"]);
      new_option.attr("value", city["id"]);
      select.append(new_option);
    }
    $("#location-modal .modal-body").append(select);
  });
}

function getWeatherState() {
  $.post($SCRIPT_ROOT + "/weather/getWeatherState", {
    "cityCode": $("select").val()
  }, function (data) {
    $("#clock").parent().append($(data));
    location_modal.toggle();
  })
}