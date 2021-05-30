from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

BOARD = "board"
NUM_PLAYS = "nplays"
HIGH_SCORE = "highscore"

class FlaskTests(TestCase):
    
    def setUp(self):
        """Test setup."""
        self.client = app.test_client()
        app.config['TESTING'] = True
        
    def test_homepage(self):
        with self.client:
            resp = self.client.get('/')   
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Score:', html)
            self.assertIn('Seconds Left:', html)
            self.assertIn('Highest Score:', html)
            self.assertIn('Number of plays:', html)
            
            self.assertIn(BOARD, session) 
            self.assertIsNone(session.get(HIGH_SCORE))
            self.assertIsNone(session.get(NUM_PLAYS))
            
    def test_check_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[BOARD] = [["T", "E", "T", "T", "E"], 
                                 ["E", "S", "D", "A", "T"], 
                                 ["A", "T", "T", "Y", "T"], 
                                 ["S", "A", "B", "T", "R"], 
                                 ["P", "A", "T", "U", "T"]]
            resp = self.client.get('/check-word?word=test')   
            
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'ok') 
            
    def test_check_invalid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[BOARD] = [["T", "T", "T", "T", "T"], 
                                 ["T", "T", "T", "T", "T"], 
                                 ["A", "T", "T", "Y", "T"], 
                                 ["A", "T", "T", "T", "T"], 
                                 ["T", "T", "T", "T", "T"]]
            resp = self.client.get('/check-word?word=taat')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-word') 
            
    def test_check_not_on_board_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[BOARD] = [["T", "T", "T", "T", "T"], 
                                 ["T", "T", "T", "T", "T"], 
                                 ["A", "T", "T", "Y", "T"], 
                                 ["A", "T", "T", "T", "T"], 
                                 ["T", "T", "T", "T", "T"]]
            resp = self.client.get('/check-word?word=cat')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-on-board')                               