
var correct_answer = ''  ///< the correct answer

/**
  Load JSON from server
*/
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

/**
  Get indices of placeholders to wrap
*/
function indices(txt) {
    //console.log(txt)
    var res = []
    var i = 0
    while (i>=0) {
      var ind = txt.indexOf("...", i)
      if (ind>=0)
      {
        res.push(ind)
        i = ind+1
      }
      else
        i = -1
    }
    return res
}

/**
  Parse JSON data
*/
function parseData(data) {
    //alert(data)
    var obj = JSON.parse(data)
    var txt = obj.question
    
    var inds = indices(txt)
    inds.reverse()
    var j = inds.length
    inds.forEach (function(i){
        //console.log(i)
        var placeh = `<span id='answer${j}' class='emph'>...</span>`
        txt = txt.substr(0, i) + placeh + txt.substr(i+3)
        j = j - 1
    })
    document.getElementById("question").innerHTML = txt

    correct_answer = obj.answer
    var sel = document.getElementById("selector")
    while (sel.firstChild) {
        sel.removeChild(sel.firstChild);
    }

    //obj.variants.unshift(correct_answer)
    obj.variants.unshift("")

    obj.variants.forEach(element => {
        //console.log(element)
        var opt = document.createElement('option');
        opt.innerText = element;
        sel.appendChild(opt)
    });
}

/**
  Insert answer instead of placeholder when the variant is chosen
*/
function onVerbChosen(value) {
    a1 = document.getElementById("answer1")
    a2 = document.getElementById("answer2")
    if (a2=== null) {
        a1.innerText = value
    }
    else {
        values = value.split(" ")
        if (values.length==2)
        {
            a1.innerText = values[0]
            a2.innerText = values[1]
        }
    }
}

/**
  Verify the user's answer
*/
function verify() {
    var a1 = document.getElementById("answer1")
    var a2 = document.getElementById("answer2")
    var answer = a1.innerText
    if( a2!==null )
      answer = answer + " " + a2.innerText
    
    var img = document.getElementById("state")
        
    if( answer.toLowerCase()===correct_answer.toLowerCase())
        img.src = "ok.png"
    else
        img.src = "fail.png"
}

/**
  Request new exercise
*/
function newExercise() {
    var img = document.getElementById("state")
    img.src = ""
    loadJSON("")
}
