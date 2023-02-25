let frontField = $('#front')[0]
let backField = $('#back')[0]
let frontForm = $('#front-form')[0]
let backForm = $('#back-form')[0]
let previewer = $('#preview')[0]

window.onload = init
function init() {
    frontField.innerText = frontForm.value
    backField.innerText = backForm.value
    onEditorInput()
}

function onEditorInput() {
    console.log('lol:' + backField.value)
    frontForm.value = frontField.innerText
    backForm.value = backField.innerText
    previewer.src = "/card_preview?" + "front=" + encodeURIComponent(frontForm.value) + "&back=" + encodeURIComponent(backForm.value)
}