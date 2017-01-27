function response_callback(response, elem) {
        const element = document.getElementById(elem);
        if (elem == "Battery") {
            response = response / 255. * 3.3 * 10.;
            response = response.toFixed(2)  + "V";
            setSensorValue("INF7", response);
        }
        if (["INF1", "INF2", "INF3", "INF4", "INF5", "INF6"].includes(elem)) {
            setSensorValue(elem, response);
        }
        element.innerHTML = elem + ": " + response;
    }
    function request(cmd, elem="Status") {
        const req = new XMLHttpRequest();
        req.open('GET', 'cgi-bin/request.py?cmd='+cmd, true);
        req.onload = function() {
            if (req.status == 200) {
                response_callback(req.responseText, elem);
            }
        }
        req.send(null);
    }
    function setSensorValue(sensor, value) {
        const a = document.getElementById("sensor_svg");
        const svg = a.contentDocument;
        const item = svg.getElementById(sensor);
        item.innerHTML = value;
    }
    function battary_timeout_callback() {
        request("A", "Battery");
        setTimeout("battary_timeout_callback();", 17000);
    }

    let ir = 1;

    function sensor_timeout_callback() {
        request(ir.toString(), "INF" + ir);
        ir += 1;
        if (ir > 7) ir = 1;
        setTimeout("sensor_timeout_callback();", 250);
    }
    function main() {
        battary_timeout_callback();
        sensor_timeout_callback();
    }
