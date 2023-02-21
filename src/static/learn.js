let cards = $(".card")
let current_card = 0
let num_cards = cards.length

cards[0].hidden = false

function showNextCard() {
    cards[current_card].hidden = true
    if (current_card < num_cards - 1) {
        current_card += 1
        cards[current_card].hidden = false
    } else{
        $('#learning-complete')[0].hidden = false
    }
}

function showAnswer(id) {
    let back = document.getElementById('back' + id)
    back.hidden = false
}

function sendResult(result, id) {
    console.log('Answer ', result, 'on question ', id)
    $.post('/make_answer',
        {
            card_id: id,
            result: result
        },
        callback
    )
    showNextCard()
}
