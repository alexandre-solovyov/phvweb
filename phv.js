
var correct_answer = ''

function loadJSON(file) {
    var request = new XMLHttpRequest();
    request.open('GET', file, true);
    request.send(null);
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader('Content-Type');
            if (type.indexOf("text") !== 1) {
                parseData(request.responseText);
            }
        }
    }
}

function parseData(data) {
    var obj = JSON.parse(data)
    var txt = obj.question
    txt = txt.replace("...", "<span id='answer' class='emph'>...</span>")
    document.getElementById("question").innerHTML = txt

    correct_answer = obj.answer
    var sel = document.getElementById("selector")
    while (sel.firstChild) {
        sel.removeChild(sel.firstChild);
    }

    obj.variants.unshift(correct_answer)
    obj.variants.unshift("")

    obj.variants.forEach(element => {
        //console.log(element)
        var opt = document.createElement('option');
        opt.innerText = element
        sel.appendChild(opt)
    });
}

function verb_chosen(value) {
    document.getElementById("answer").innerText = value
}

function verify() {
    var answer = document.getElementById("answer").innerText
    var img = document.getElementById("state")
        
    if( answer===correct_answer)
        img.src = "ok.png"
    else
        img.src = "fail.png"
}

