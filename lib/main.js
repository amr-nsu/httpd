const robot1='http://192.168.0.104:8000'; 
const robot2='http://192.168.0.103:8000';

function response_callback(response, elem) {
        const element = document.getElementById(elem);
        if (elem == "Battery") {
            response = response + " V";
            setSensorValue("INF7", response);
        }

        if (["INF1", "INF2", "INF3", "INF4", "INF5", "INF6"].includes(elem)) {
            setSensorValue(elem, response);
        }
        element.innerHTML = elem + ": " + response;
    }
    function request(ip, cmd, elem="Status") {
        const req = new XMLHttpRequest();
        req.open('GET', ip+'/cmd='+cmd, true);
        req.onload = function() {
            if (req.status == 200) {
                response_callback(req.responseText, elem);
            }
        }
        req.send(null);
    }

    function request1(cmd) {
        request(robot1, cmd);
        request2(cmd);
    }   
    function request2(cmd) {
        request(robot2, cmd);
    }   
    

    function setSensorValue(sensor, value) {
        const a = document.getElementById("sensor_svg");
        const svg = a.contentDocument;
        const item = svg.getElementById(sensor);
        item.innerHTML = value;
    }
    function battary_timeout_callback() {
        request(robot1, "A", "Battery");
        setTimeout("battary_timeout_callback();", 10000);
    }
    function coordinates_timeout_callback() {
        request(robot1, "C", "Coordinates");
        setTimeout("coordinates_timeout_callback();", 1000);
    }

    let ir = 1

    function sensor_timeout_callback() {
        request(robot1, ir.toString(), "INF" + ir);
        ir += 1;
        if (ir > 6) ir = 1;
        setTimeout("sensor_timeout_callback();", 50);
    }
    function main() {
        coordinates_timeout_callback();
        battary_timeout_callback();
        sensor_timeout_callback();
    }

    function go(){
        let a = document.getElementById("posx").value;
        let b = document.getElementById("posy").value;
        request(robot1, "go&x=" + a +"&y=" + b);

    }
