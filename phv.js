
var correct_answer = ''

function loadJSON() {
    var request = new XMLHttpRequest();
    request.open('GET', 'new_ex', true);
    request.send();
    request.onreadystatechange = function () {
        //alert(request.readyState)
        //alert(request.status)
        if (request.readyState === 4 && request.status === 200) {
            var type = request.getResponseHeader('Content-type');
            //alert(type)
            if (type.indexOf("json") !== 1) {
                parseData(request.responseText);
            }
        }
    }
}

function parseData(data) {
    //alert(data)
    var obj = JSON.parse(data)
    var txt = obj.question
    txt = txt.replace("...", "<span id='answer' class='emph'>...</span>")
    document.getElementById("question").innerHTML = txt

    correct_answer = obj.answer
    var sel = document.getElementById("selector")
    while (sel.firstChild) {
        sel.removeChild(sel.firstChild);
    }

    //obj.variants.unshift(correct_answer)
    obj.variants.unshift("")

    obj.variants.forEach(element => {
        console.log(element)
        var opt = document.createElement('option');
        opt.innerText = element;
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

function newex() {
    var img = document.getElementById("state")
    img.src = ""
    loadJSON("")
}