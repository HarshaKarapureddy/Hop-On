# Harsha Karapureddy
# CS 3354
# Group 6
# File Description: Tests write_review.py file and EMPTIES IT WHEN TESTED

import unittest
import sqlite3
from write_review import clear_reviews_all, db_write_review, db_edit_review, db_delete_review, db_view_reviews, valid_userID, valid_gameID, valid_rating

class test_write_review(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect("reviews.db")  # Creates a temporary database in RAM
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                reviewID INTEGER PRIMARY KEY AUTOINCREMENT,
                userID INTEGER NOT NULL,
                gameID INTEGER NOT NULL,
                gameName TEXT NOT NULL,
                rating FLOAT NOT NULL,
                reviewText TEXT NOT NULL
            )
        ''')
        cls.conn.commit()

    def setUp(self):
        clear_reviews_all()
        self.conn.commit()

    # TEST CASES

    # TC1
    def test_write_review(self):
        result = db_write_review(123456, 1001, "Outlast", 4.5, "Great game!")   
        self.assertEqual(result, "Review Added!")                               

        #check
        self.cursor.execute("SELECT * FROM reviews WHERE userID = ?", (123456,))
        data = self.cursor.fetchall()
        self.assertEqual(len(data), 1)
        
    # TC2
    def test_invalid_usrID(self):
        result = db_write_review(1234, 1001, "Outlast", 4.5, "Great game!")   
        self.assertEqual(result, "Error: Invalid UserID")                               

        #check
        self.cursor.execute("SELECT * FROM reviews WHERE userID = ?", (123456,))
        data = self.cursor.fetchall()
        self.assertEqual(len(data), 0)
    
    # TC3
    def test_invalid_gameID(self):
        result = db_write_review(123456, -45, "Outlast", 4.5, "Great game!")   
        self.assertEqual(result, "Error: Invalid gameID")                               

        #check
        self.cursor.execute("SELECT * FROM reviews WHERE userID = ?", (123456,))
        data = self.cursor.fetchall()
        self.assertEqual(len(data), 0)

    # TC4
    def test_invalid_rating(self):
        result = db_write_review(123456, 45, "Outlast", 60000, "Great game!")   
        self.assertEqual(result, "Error: Invalid rating")                               

        #check
        self.cursor.execute("SELECT * FROM reviews WHERE userID = ?", (123456,))
        data = self.cursor.fetchall()
        self.assertEqual(len(data), 0)

    # TC5
    def test_invalid_reviewID(self):
        db_write_review(123456, 1001, "Baldur's Gate 3", 4.5, "Great game!")
        
        self.cursor.execute("SELECT reviewID FROM reviews WHERE userID = ?", (123456,))
        reviewID = self.cursor.fetchone()[0]

        # INVALID ID INSERETED HERE
        result = db_edit_review(123456, str(-50), 5.0, "Awesome game!")
        self.assertEqual(result, "Error: Invalid ReviewID")

    # TC6
    def test_edit_review(self):
        db_write_review(123456, 1001, "Baldur's Gate 3", 4.5, "Great game!")
        
        self.cursor.execute("SELECT reviewID FROM reviews WHERE userID = ?", (123456,))
        reviewID = self.cursor.fetchone()[0]

        result = db_edit_review(123456, str(reviewID), 5.0, "Awesome game!")
        self.assertEqual(result, "Edit Made!")

        #check
        self.cursor.execute("SELECT rating, reviewText FROM reviews WHERE reviewID = ?", (reviewID,))
        data = self.cursor.fetchone()
        self.assertEqual(data, (5.0, "Awesome game!"))
        
    # TC7
    def test_delete_review(self):
        db_write_review(123456, 1001, "Marvel Rivals", 4.5, "Great game!")

        self.cursor.execute("SELECT reviewID FROM reviews WHERE userID = ?", (123456,))
        reviewID = self.cursor.fetchone()[0]
        

        result = db_delete_review(123456, str(reviewID))
        self.assertEqual(result, "Review Removed!")

        #check
        self.cursor.execute("SELECT * FROM reviews WHERE reviewID = ?", (reviewID,))
        data = self.cursor.fetchone()
        self.assertIsNone(data)
        
    # TC8
    def test_view_review(self):
        db_write_review(123456, 1001, "Far Cry 4", 4.5, "Great game!")
        db_write_review(123456, 1002, "It Takes Two", 3.0, "Okay game")

        result = db_view_reviews(123456)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        
    
    @classmethod
    def tearDownClass(cls):
        clear_reviews_all()
        cls.conn.close()

if __name__ == '__main__':
    unittest.main()
    clear_reviews_all()