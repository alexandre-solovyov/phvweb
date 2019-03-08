
var nbVerbs = 5
var verbs = []
var start = 0
var current_shift = 0
var current_delta = 0
var current_verb = ""
var parts = []

/**
  Load any JSON information from the server
*/
function loadJSON(command, func) {
    var request = new XMLHttpRequest();
    request.open('GET', command, true);
    request.send();
    request.onreadystatechange = function () {
        //alert(request.readyState)
        //alert(request.status)
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader('Content-type');
            //alert(type)
            if (type.indexOf("json") !== 1) {
                func(request.responseText);
            }
        }
    }
}

/**
  Load all verbs information
*/
function loadAllVerbs() {
    loadJSON('verbs', showVerbs)
}

/**
  Load verb information
*/
function loadVerb(verb) {
    loadJSON('verb=' + verb, function(text) { showVerb(verb, text);})
}

/**
  Load verb definition
*/
function loadDefinition(part) {
    loadJSON('def=' + current_verb + " " + part, showDefinition)
}

/**
  Show all verbs information
*/
function showVerbs(data) {
    var obj = JSON.parse(data)
    verbs = obj.verbs
    showAllVerbs()
}

/**
  Show verb information
*/
function showVerb(verb, data) {

    var obj = JSON.parse(data)
    parts = obj.particles
    //console.log(verb, parts)

    // Load and show the verb meaning
    current_verb = verb
    var current_shift = 0
    var current_delta = 0
    createPrs(verb.toUpperCase(), parts)
    locate(parts.length, 0)

    loadDefinition(parts[0])
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
    while(defineul.firstChild)
        defineul.removeChild(defineul.firstChild)

    var i;
    for (i = 0; i < defs.length; i++) {
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
    var ww = Math.min(w / 2, h - 100)
    var k = 0.5
    //console.log(ww)
    var x0 = ww * k, y0 = 100 + ww * k, r1 = x0 * 3 / 4, r2 = x0 / 4

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

/**
  Create buttons for verbs
*/
function createVerbsBtns(nb) {
    var div = document.getElementById("verbs");
    while (div.firstChild)
        div.removeChild(div.firstChild)

    for (i = 0; i < nb + 2; i++) {
        b = document.createElement("button");
        b.classList.add("verb")
        if (i == 0) {
            b.innerHTML = "&#9668;"
            b.onclick = previous
        }
        else if (i == nb + 1) {
            b.innerHTML = "&#9658;"
            b.onclick = next
        }
        else {
            b.innerHTML = ""
            b.onclick = function () { selectVerb(this.innerHTML) }
        }
        div.appendChild(b)
    }
}

/**
  Show all verbs in the buttons
*/
function showAllVerbs() {
    var div = document.getElementById("verbs");
    for (i = 0; i < nbVerbs + 2; i++)
        if (i > 0 && i < nbVerbs + 1)
            div.children[i].innerHTML = verbs[start + i - 1]
    //console.log(verbs)
    selectVerb(verbs[start])    
}

/**
  Choose previous verb
*/
function previous() {
    start = start - 1
    if (start < 0)
        start = 0
    showAllVerbs()
}

/**
  Choose next verb
*/
function next() {
    start = start + 1
    if (start > verbs.length - nbVerbs)
        start = verbs.length - nbVerbs
    showAllVerbs()
}

/**
  Treat the selection of one verb
*/
function selectVerb(verb) {
    loadVerb(verb)
}

/**
  Create all buttons for verbs
*/
function createVerbs() {
    createVerbsBtns(nbVerbs)
    loadAllVerbs()
}
