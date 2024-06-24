function getExt(){
    if ("{{ file|escapejs }}".endsWith(".html")) {           
        return "django"
    }
    if ("{{ file|escapejs }}".endsWith(".py") || "{{ file|escapejs }}"=="None") {
        return "python"
    }   
    if ("{{ file|escapejs }}".endsWith(".js")) {
        return "javascript"
    }   
    if ("{{ file|escapejs }}".endsWith(".css")) {
        return "css"
    }      
}
var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
lineNumbers: true,
mode: getExt(),
indentUnit: 2,
indentWithTabs: true,
theme: "mdn-like",
lineSeparator :'\n',
});

function runCode(ischeck) {
// Get the code from the CodeMirror editor
var code = editor.getValue();
fetch('{% url "interpreter" %}', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': '{{ csrf_token }}'
    },
    body: new URLSearchParams({code: code})
})
.then(response => response.json())  
.then(data => {
    if (data.result) {
        document.getElementById('result').innerText += 'Output: ' + data.result;
    } else if (data.error) {
        document.getElementById('result').innerText += 'Error: ' + data.error;
    }
    if (ischeck){
        let true_res = '{{assignment.result|escapejs}}'
        let user_res = data.result.repla
        console.log(true_res.length)
        console.log(user_res.length)
        if (data.result == '{{assignment.result|escapejs}}'){
            //alert("Верное решение!");
        } else {
            //alert("Неверное решение.");
        }
    }
})
.catch(error => {
    document.getElementById('result').innerText += 'Request failed: ' + error;
});
}

function saveFile(){
document.getElementById('code_output').value =(JSON.stringify(editor.getValue()))
console.log(JSON.stringify(editor.getValue()));
}

function createFile(){
var file = prompt("Enter file name");
var xhr = new XMLHttpRequest();
var url = '/editor?file=' + file + "&isnew=true";
xhr.open('GET', url, true);
xhr.onload = function (e) {
    if (xhr.readyState === 4) {
        if (xhr.status === 200) {
            console.log(xhr.responseText);
        } else {
            console.error(xhr.statusText);
        }
    }
};
xhr.onerror = function (e) {
    console.error(xhr.statusText);
};
xhr.send(null);
}