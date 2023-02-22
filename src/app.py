from flask import Flask, render_template, request, redirect, url_for, send_from_directory

from storage import Storage

app = Flask(__name__)
storage = Storage()  # '/home/aeek/dev/meme/src/tmp/'


# storage.setup()

@app.route('/')
def index():
	decks = storage.get_decks()
	return render_template("index.html", decks=decks)


@app.route('/all_card')
def all_cards():
	cards = storage.get_all_cards()
	return render_template("view_cards.html", cards=cards)


@app.route('/view/<deck_name>')
def view_deck(deck_name: str):
	cards = storage.get_cards_by_deck(deck_name)
	return render_template("view_cards.html", cards=cards, deck_name=deck_name)


@app.route('/learn/<deck_name>')
def learn_deck(deck_name: str):
	cards_to_learn = storage.get_cards_to_learn_by_deck(deck_name)
	return render_template("learn_deck.html", cards=cards_to_learn, deck_name=deck_name)


@app.route('/card_editor', methods=["POST", "GET"])
def card_editor():
	decks = storage.get_decks()
	if request.method == 'GET':
		card_id = request.args.get('card_id')
		if card_id:  # Edit existing card
			card = storage.get_card_by_id(card_id)
			deck_name = card.deck_name
			return render_template("card_editor.html", deck_name=deck_name, decks=decks, card_id=card_id,
								   front=card.front, back=card.back)
		else:  # Create new card
			deck_name = request.args.get('deck_name')
			return render_template("card_editor.html", deck_name=deck_name, decks=decks)
	elif request.method == 'POST':
		deck_name = request.form.get('deck_name')
		front = request.form.get('front')
		back = request.form.get('back')
		card_id = request.form.get('card_id', type=int)
		if card_id:
			storage.edit_card(card_id, deck_name, front, back)
		else:
			card_id = storage.create_card(deck_name, front, back)
		return render_template("card_editor.html", deck_name=deck_name, decks=decks, card_id=card_id, front=front,
							   back=back)


@app.route('/new_deck', methods=["POST"])
def new_deck():
	deck_name = request.form.get('deck_name')
	success = storage.create_deck(deck_name)
	return {'success': success}


@app.route('/make_answer', methods=["POST"])
def handle_answer():
	card_id = request.form.get('card_id')
	result = request.form.get('result')
	if card_id and result:
		print(f'<{card_id}> : {result}')
		result = int(result)
		if result >= 3:
			storage.learn_card(result, card_id)
	return 'ok'


@app.route('/card_preview')
def card_preview():
	front = request.args.get('front')
	back = request.args.get('back')
	print(front, back)
	return render_template('card_preview.html', front=front, back=back)


@app.route('/delete_card', methods=["POST"])
def delete_card():
	card_id = request.form.get('card_id', type=int)
	storage.delete_card(card_id)
	return 'ok'


@app.route('/delete_deck', methods=["POST"])
def delete_deck():
	deck_name = request.form.get('deck_name')
	storage.delete_deck(deck_name)
	return 'ok'
