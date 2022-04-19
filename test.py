from unittest import TestCase
from flask import session
from app import app
from boggle import Boggle

app.config["testing"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_home(self):
        with self.client as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('board', session)
            self.assertIn('<p> Score:', html)
            self.assertIn('<p> Time:', html)
            self.assertIn('<p> High Score:', html)
            self.assertIn('<table id="board">', html)
            self.assertIn('<button type="submit">New Game</button>', html)


    def test_valid_words(self):
        """Test valid words with different directions on the board"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess["board"] = [["C", "R", "O", "W", "N"],
                                 ["O", "A", "T", "I", "I"],
                                 ["C", "M", "K", "R", "L"],
                                 ["T", "I", "M", "E", "B"],
                                 ["P", "A", "L", "V", "S"]]

        res1 = self.client.get("/check-word?word=crown")
        res2 = self.client.get("/check-word?word=cake")
        res3 = self.client.get("/check-word?word=wire")

        self.assertEqual(res1.json['result'], 'ok')
        self.assertEqual(res2.json['result'], 'ok')
        self.assertEqual(res3.json['result'], 'ok')


    def test_not_on_board(self):
        """Test a word that is not on board"""
        self.client.get("/")
        res = self.client.get("/check-word?word=hello")
        self.assertEqual(res.json['result'], 'not-on-board')


    def test_not_in_dictionary(self):
        """Test a word that is not in dictionary"""
        self.client.get("/")
        res = self.client.get("/check-word?word=lmkto")
        self.assertEqual(res.json['result'], 'not-word')
