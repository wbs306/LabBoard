function calcCoordinates(height, width, values) {
  const min = Math.min.apply(null, values) * 0.8;
  const max = Math.max.apply(null, values) * 1.2;

  const yRatio = (max - min) / height;
  const xRatio = width / values.length;

  return values.map((value, i) => {
      const y = height - (value - min) / yRatio || 0;
      const x = xRatio * i;
      return [x, y];
  });
}

function getMidPoint(Ax, Ay, Bx, By) {
  const Zx = (Ax + Bx) / 2;
  const Zy = (Ay + By) / 2;
  return [Zx, Zy];
}

function getPath(points) {
  const SPACE = ' ';
  let next; let Z;
  const X = 0;
  const Y = 1;
  let path = '';
  let point = points[0];

  path += 'M' + point[X] + ',' + point[Y];
  const first = point;

  for (let i = 0; i < points.length; i++) {
      next = points[i];
      Z = getMidPoint(point[X], point[Y], next[X], next[Y]);
      path += SPACE + Z[X] + ',' + Z[Y];
      path += ' Q' + Math.floor(next[X]) + ',' + next[Y];
      point = next;
  }

  const second = points[1];
  Z = getMidPoint(first[X], first[Y], second[X], second[Y]);
  path += SPACE + points[points.length - 1];
  return path;
}

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

function setGraphic(card_name, values, g_config) {
  let margin_top = $(card_name + " .card-info").css("margin-top");
  let height = $(card_name + " .card-body").height() - $(card_name + " .card-info").height() - parseFloat(margin_top.slice(0, margin_top.length - 2));
  let width = $(card_name + " .line-chart").width() + 30;

  let line_svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  line_svg.setAttribute("height", height);
  line_svg.setAttribute("width", "100%");

  let line_path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  line_path.setAttribute("fill", g_config["fill"]);
  line_path.setAttribute("stroke", g_config["line"]);
  line_path.setAttribute("stroke-width", g_config["line_width"]);
  line_path.setAttribute("stroke-linecap", g_config["linecap"]);
  let path = getPath(calcCoordinates(height, width, values));
  line_path.setAttribute("d", path + " V " + width + " H 0")

  line_svg.append(line_path);
  $(card_name + " .line-chart").append(line_svg);
}
