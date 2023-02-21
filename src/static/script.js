
function new_deck() {
    let name = prompt('Enter deck name:', '')
    if (name.length > 0) {
        $.post('/new_deck',
            {
                deck_name: name
            },
            onNewDeckResult
        )
    }
}

function onNewDeckResult(data) {
    if (!data.success) {
        alert("Deck with the same name already exists!")
    }
}

function deleteCard(card_id) {
    $.post('/delete_card',
        {
            card_id: card_id
        },
        callback
    )
}

function deleteDeck(deck_name) {
    let status = confirm("Do you want to delete " + deck_name + " deck?")
    if (status) {
        $.post('/delete_deck',
            {
                deck_name: deck_name
            },
            callback
        )
    }
}

function callback(data) {
    console.log("Got data: " + data)
}
