
var current_shift = 0
var current_delta = 0

function loadJSON() {
    var verb = "GET"
    var parts = ["at", "away", "on", "up", "off"]
    createPrs(verb, parts)
    locate(parts.length, 0)
}

function circ(elem, x0, y0, r, bord, fsize) {
    elem.style.left = Math.round(x0 - r) + "px"
    elem.style.top = Math.round(y0 - r) + "px"
    elem.style.width = Math.round(2 * r) + "px"
    elem.style.height = Math.round(2 * r) + "px"
    elem.style.border = bord + "px solid white"
    elem.style.borderRadius = Math.round(r) + "px"
    elem.style.font = fsize + "pt Times"
}

function createPrs(verb, parts) {
    var main = document.getElementById("main");
    main.innerText = verb

    var n = parts.length
    for (var i = 0; i < n; i++) {
        var b = document.createElement("button");
        b.id = "part" + (i + 1)
        b.index = i
        b.nbItems = n
        b.classList.add("part")
        b.innerText = parts[i]
        b.onclick = function () { onSelect(this.index, this.nbItems, this.innerText) }
        document.body.appendChild(b)
    }
}

function locate(n, shift) {
    var w = document.body.clientWidth
    var h = document.body.clientHeight
    var x0 = w / 4, y0 = 100 + w / 4, r1 = x0 * 3 / 4, r2 = x0 / 4

    var define = document.getElementById("define");
    define.style.top = (y0-50) + "px"

    var main = document.getElementById("main");
    circ(main, x0, y0, r1, 0, 60)

    var d = 2.0 * Math.PI / n
    current_delta = d

    for (var i = 0; i < n; i++) {
        var b = document.getElementById("part" + (i + 1));
        var a = d * i + shift
        circ(b, x0 + r1 * Math.cos(a), y0 + r1 * Math.sin(a), r2, 8, 20)
    }

    current_shift = shift
}

function animate(draw, duration) {
    var start = performance.now();
    requestAnimationFrame(function animate(time) {
        var timePassed = time - start;
        if (timePassed > duration) timePassed = duration;
        draw(timePassed);
        if (timePassed < duration) {
            requestAnimationFrame(animate);
        }
    });
}

function onSelect(index, n, part) {
    //console.log(index + " " + part)

    var time = 500
    var main = document.getElementById("main");
    var start_shift = current_shift
    var new_shift = -current_delta * index
    var delta = new_shift - start_shift
    if (delta > Math.PI)
        delta = delta - 2 * Math.PI
    if (delta < -Math.PI)
        delta = delta + 2 * Math.PI
    //console.log(delta)

    //locate(n, new_shift)
    var step = delta / time
    animate(function (timePassed) {
        var shift = start_shift + step * timePassed
        //console.log(shift)
        locate(n, shift)
    }, time);
}
