
var current_shift = 0
var current_delta = 0
var current_verb = ""
var parts = []

/**
  Load verb information
*/
function loadVerb(verb) {
    var request = new XMLHttpRequest();
    request.open('GET', 'verb='+verb, true);
    request.send();
    request.onreadystatechange = function () {
        //alert(request.readyState)
        //alert(request.status)
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader('Content-type');
            //alert(type)
            if (type.indexOf("json") !== 1) {
                showVerb(verb, request.responseText);
            }
        }
    }
}

/**
  Load verb definition
*/
function loadDefinition(part) {
    var request = new XMLHttpRequest();
    //console.log(current_verb, part)
    request.open('GET', 'def=' + current_verb + " " + part, true);
    request.send();
    request.onreadystatechange = function () {
        //alert(request.readyState)
        //alert(request.status)
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader('Content-type');
            //alert(type)
            if (type.indexOf("json") !== 1) {
                showDefinition(request.responseText);
            }
        }
    }
}

/**
  Show verb information
*/
function showVerb(verb, data) {

    var obj = JSON.parse(data)
    parts = obj.particles
    //console.log(parts)

    current_verb = verb
    createPrs(verb.toUpperCase(), parts)
    locate(parts.length, 0)
}

/**
  Clear verb definition
*/
function clearDefinition() {
    var defineul = document.getElementById("define");
    while (defineul.firstChild)
        defineul.removeChild(defineul.firstChild)
}

/**
  Show verb definition
*/
function showDefinition(data) {

    var obj = JSON.parse(data)
    var defs = obj.definition
    //console.log(defs)

    var defineul = document.getElementById("define");

    var i;
    for (i = 0; i<defs.length; i++)
    {
        var item = document.createElement("li");
        item.innerText = defs[i];
        defineul.appendChild(item)
    }
}

/**
  Build circular element
*/
function circ(elem, x0, y0, r, bord) {
    elem.style.left = Math.round(x0 - r) + "px"
    elem.style.top = Math.round(y0 - r) + "px"
    elem.style.width = Math.round(2 * r) + "px"
    elem.style.height = Math.round(2 * r) + "px"
    elem.style.border = bord + "px solid white"
    elem.style.borderRadius = Math.round(r) + "px"
}

/**
  Create elements for verb with particles
*/
function createPrs(verb, parts) {
    var main = document.getElementById("main");
    main.innerText = verb

    var partsdiv = document.getElementById("parts");
    while (partsdiv.firstChild) {
        partsdiv.removeChild(partsdiv.firstChild);
    }

    var n = parts.length
    for (var i = 0; i < n; i++) {
        var b = document.createElement("button");
        b.id = "part" + (i + 1)
        b.index = i
        b.nbItems = n
        b.classList.add("part")
        b.innerText = parts[i]
        b.onclick = function () { onSelect(this.index, this.nbItems, this.innerText) }
        partsdiv.appendChild(b)
    }
}

/**
  Locate the elements for verb with particles
*/
function locate(n, shift) {
    var w = document.documentElement.clientWidth
    var h = document.documentElement.clientHeight
    var ww = Math.min(w/2, h-100)
    var k = 0.5
    //console.log(ww)
    var x0 = ww*k, y0 = 100 + ww*k, r1 = x0 * 3 / 4, r2 = x0 / 4

    //var define = document.getElementById("define");
    //define.style.top = (y0-50) + "px"

    var main = document.getElementById("main");
    circ(main, x0, y0, r1, 0)

    var d = 2.0 * Math.PI / n
    current_delta = d

    for (var i = 0; i < n; i++) {
        var b = document.getElementById("part" + (i + 1));
        var a = d * i + shift
        circ(b, x0 + r1 * Math.cos(a), y0 + r1 * Math.sin(a), r2, 8)
    }

    current_shift = shift
}

/**
  Animate the elements
*/
function animate(draw, duration, func_after_finish) {
    var start = performance.now();
    requestAnimationFrame(function animate(time) {
        var timePassed = time - start;
        if (timePassed > duration) {
            timePassed = duration;
            //console.log("finish")
            func_after_finish()
        }
        draw(timePassed);
        if (timePassed < duration) {
            requestAnimationFrame(animate);
        }
    });
}

/**
  Treat the selection
*/
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
    clearDefinition()
    animate(function (timePassed) {
        var shift = start_shift + step * timePassed
        //console.log(shift)
        locate(n, shift)
    }, time, function () {
        loadDefinition(parts[index])
    });
}
