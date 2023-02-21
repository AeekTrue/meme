let frontField = $('#front')[0]
let backField = $('#back')[0]
let previewer = $('#preview')[0]

onEditorInput()
function onEditorInput(){
    console.log('lol:' + backField.value)
    previewer.src = "/card_preview?" + "front=" + encodeURIComponent(frontField.value) + "&back=" + encodeURIComponent(backField.value)
}