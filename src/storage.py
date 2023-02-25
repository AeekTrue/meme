import os
import sqlite3 as sql
from json import load
from pathlib import Path
from collections import namedtuple
from sm2_algo import sm2
from datetime import datetime as dt, timedelta


def namedtuple_factory(cursor, row):
	"""
	Usage:
	con.row_factory = namedtuple_factory
	"""
	fields = [col[0] for col in cursor.description]
	Row = namedtuple("Row", fields)
	return Row(*row)


class Card:
	def __init__(self, path: Path):
		self.path = path
		with open(path) as f:
			self.json = load(f)


class Deck:
	def __init__(self, path: Path):
		self.name = path.name


class Storage:
	def __init__(self, path: str = None):
		self.path = Path(path or os.path.expanduser('~'), '.meme')
		self.db_path = Path(self.path, 'data.db')
		print(self.path)
		if not os.path.exists(self.path):
			os.makedirs(self.path)
		if not os.path.exists(self.db_path):
			self.setup()

	def setup(self):
		script_path = Path(Path(__file__).parent, 'setup.sql')
		with open(script_path) as f:
			script = f.read()
			with sql.connect(self.db_path) as con:
				cur = con.cursor()
				cur.executescript(script)
				con.commit()

	# test_fill(self)

	def get_all_cards(self):
		with sql.connect(self.db_path) as con:
			con.row_factory = namedtuple_factory
			cur = con.cursor()
			cur.execute("SELECT * FROM card ORDER BY deck_name, front")
			return cur.fetchall()

	def get_decks(self):
		with sql.connect(self.db_path) as con:
			con.row_factory = namedtuple_factory
			cur = con.cursor()
			cur.execute(
				"""
				SELECT name, count(c.id) cards, sum(c.next_review <= date('now')) to_learn
				from deck d
					left join card c on d.name = c.deck_name
				GROUP BY d.name
				ORDER BY to_learn DESC, cards DESC, name
				"""
			)
			return cur.fetchall()

	def create_deck(self, deck_name: str):
		name_exists = self.deck_name_exists(deck_name)
		if not name_exists:
			with sql.connect(self.db_path) as con:
				cur = con.cursor()
				cur.execute("INSERT INTO deck(name) VALUES (?)", (deck_name,))
				con.commit()
				return True
		else:
			return False

	def create_card(self, deck_name, front, back):
		with sql.connect(self.db_path) as con:
			cur = con.cursor()
			cur.execute(
				"INSERT INTO card(front, back, deck_name) VALUES (?, ?, ?)", (front, back, deck_name)
			)
			card_id = cur.lastrowid
			return card_id

	def get_cards_by_deck(self, deck_name):
		with sql.connect(self.db_path) as con:
			con.row_factory = namedtuple_factory
			cur = con.cursor()
			cur.execute(
				"SELECT * FROM card WHERE deck_name = ?", (deck_name,)
			)
			return cur.fetchall()

	def get_cards_to_learn_by_deck(self, deck_name):
		with sql.connect(self.db_path) as con:
			con.row_factory = namedtuple_factory
			cur = con.cursor()
			cur.execute(
				"SELECT * FROM card WHERE deck_name = ? and next_review <= date('now') ORDER BY RANDOM()", (deck_name,)
			)
			return cur.fetchall()

	def learn_card(self, grade, card_id):
		with sql.connect(self.db_path) as con:
			con.row_factory = namedtuple_factory
			cur = con.cursor()
			card = self.get_card_by_id(card_id)
			new_rep, new_easy, new_interval = sm2(grade, card.repetition, card.easiness, card.interval,
												  random_delta=True)
			review_date = dt.now()
			review_date_str = review_date.strftime('%Y-%m-%d')
			next_review = review_date + timedelta(days=new_interval)
			next_review_str = next_review.strftime('%Y-%m-%d')
			cur.execute(
				"""
				UPDATE card
				SET
					repetition = ?,
					easiness = ?,
					interval = ?,
					last_review = ?,
					next_review = ?
				WHERE id = ?
				""", (new_rep, new_easy, new_interval, review_date_str, next_review_str, card_id)
			)
			cur.execute(
				"""
				INSERT INTO learning(card_id, review_date, score)
				VALUES (? , ? , ?)
				""", (card_id, review_date_str, grade)
			)
			con.commit()

	def get_card_by_id(self, card_id):
		with sql.connect(self.db_path) as con:
			con.row_factory = namedtuple_factory
			cur = con.cursor()
			cur.execute(
				"SELECT * FROM card WHERE id = ?", (card_id,)
			)
			return cur.fetchone()

	def edit_card(self, card_id, deck_name, front, back):
		with sql.connect(self.db_path) as con:
			cur = con.cursor()
			cur.execute(
				"UPDATE card SET deck_name = ?, front = ?, back = ? WHERE id = ?", (deck_name, front, back, card_id)
			)
			con.commit()

	def deck_name_exists(self, deck_name):
		with sql.connect(self.db_path) as con:
			cur = con.cursor()
			cur.execute("SELECT count(id) FROM deck WHERE name = ?", (deck_name,))
			return cur.fetchone()[0] > 0

	def delete_card(self, card_id):
		with sql.connect(self.db_path) as con:
			cur = con.cursor()
			cur.execute("DELETE FROM learning WHERE card_id = ?", (card_id,))
			cur.execute("DELETE FROM card WHERE id = ?", (card_id,))
			con.commit()

	def delete_deck(self, deck_name):
		with sql.connect(self.db_path) as con:
			cur = con.cursor()
			cur.execute("DELETE FROM card WHERE deck_name = ? RETURNING card.id", (deck_name,))
			cards_to_delete = cur.fetchall()
			cur.executemany("DELETE FROM learning WHERE card_id= ?", cards_to_delete)
			cur.execute("DELETE FROM deck WHERE name = ?", (deck_name,))
			con.commit()


def test_fill(s: Storage):
	s.create_deck('test1')
	s.create_deck('привет')
	s.create_deck('test2')
	s.create_card('test1', 'lol', 'kek')


def main():
	storage = Storage('tmp/')
	# storage.create_deck('physics')
	storage.setup()


if __name__ == '__main__':
	main()
