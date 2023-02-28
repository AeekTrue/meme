let frontField = $('#front')[0]
let backField = $('#back')[0]
let frontForm = $('#front-form')[0]
let backForm = $('#back-form')[0]
let previewer = $('#preview')[0]

window.onload = init
frontField.addEventListener('keyup', onHotKey, frontField)
backField.addEventListener('keyup', onHotKey, backField)

function init() {
    frontField.innerText = frontForm.value
    backField.innerText = backForm.value
    onEditorInput()
}

function onEditorInput() {
    frontForm.value = frontField.innerText
    backForm.value = backField.innerText
    previewer.src = "/card_preview?" + "front=" + encodeURIComponent(frontForm.value) + "&back=" + encodeURIComponent(backForm.value)
}

function onHotKey(e){
    if (e.ctrlKey && e.key === '('){
        console.log('HOT KEY!!!')
        insertAtCursor(e.target, 'LoL')
    }
}

function insertAtCursor(myField, myValue) {
    console.log(myField.selectionStart)
    //IE support
    if (document.selection) {
        myField.focus();
        sel = document.selection.createRange();
        sel.text = myValue;
    }
    //MOZILLA and others
    else if (myField.selectionStart || myField.selectionStart === '0') {
        console.log('KeK')
        var startPos = myField.selectionStart;
        var endPos = myField.selectionEnd;
        myField.value = myField.value.substring(0, startPos)
            + myValue
            + myField.value.substring(endPos, myField.value.length);
    } else {
        myField.value += myValue;
    }
}
