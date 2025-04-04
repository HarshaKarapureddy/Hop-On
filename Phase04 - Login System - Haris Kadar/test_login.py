import unittest
import sqlite3
from login import login, create_user, logout, is_logged_in, get_current_user

class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n=== Setting up test database ===")
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('DELETE FROM users')
        conn.commit()
        conn.close()
        print("Database initialized successfully.\n")

    def setUp(self):
        create_user('username1', 'password1')
        create_user('adminuser', 'adminpassword')
        print(f"\n--- Starting test: {self._testMethodName} ---")

    def tearDown(self):
        logout()
        print(f"--- Finished test: {self._testMethodName} ---\n")

    def test_login_success(self):
        print("Test Case: Successful Logins")
        result1 = login('username1', 'password1')
        print("→ Input: ('username1', 'password1')")
        print(f"← Result: {result1}")
        self.assertTrue(result1)

        result2 = login('adminuser', 'adminpassword')
        print("→ Input: ('adminuser', 'adminpassword')")
        print(f"← Result: {result2}")
        self.assertTrue(result2)

    def test_login_failure(self):
        print("Test Case: Failed Logins")
        result1 = login('username1', 'wrongpassword')
        print("→ Input: ('username1', 'wrongpassword')")
        print(f"← Result: {result1}")
        self.assertFalse(result1)

        result2 = login('nonexistent', 'password123')
        print("→ Input: ('nonexistent', 'password123')")
        print(f"← Result: {result2}")
        self.assertFalse(result2)

    def test_create_user_success(self):
        print("Test Case: Successful User Creation")
        result, message = create_user('newusername', 'newpassword123')
        print("→ Creating user with username='newusername', password='newpassword123'")
        print(f"← Result: {result}, Message: {message}")
        self.assertTrue(result)

        login_result = login('newusername', 'newpassword123')
        print("→ Login attempt with new user credentials")
        print(f"← Result: {login_result}")
        self.assertTrue(login_result)

    def test_create_user_failure(self):
        print("Test Case: Failed User Creation")

        result1, message1 = create_user('username1', 'password123')
        print("→ Duplicate username attempt")
        print(f"← Result: {result1}, Message: {message1}")
        self.assertFalse(result1)

        result2, message2 = create_user('samevalue', 'samevalue')
        print("→ Username and password are the same")
        print(f"← Result: {result2}, Message: {message2}")
        self.assertFalse(result2)

        result3, message3 = create_user('short', 'password123')
        print("→ Username too short")
        print(f"← Result: {result3}, Message: {message3}")
        self.assertFalse(result3)

        result4, message4 = create_user('validusername', 'short')
        print("→ Password too short")
        print(f"← Result: {result4}, Message: {message4}")
        self.assertFalse(result4)

    def test_logout(self):
        print("Test Case: Logout Functionality")
        login('username1', 'password1')
        print("→ Logged in as 'username1'")
        
        logout_result = logout()
        print("→ Performed logout()")
        print(f"← Result: {logout_result}")
        
        is_logged_in_result = is_logged_in()
        print("→ Check is_logged_in()")
        print(f"← Result: {is_logged_in_result}")
        self.assertFalse(is_logged_in_result)

    def test_is_logged_in(self):
        print("Test Case: is_logged_in Functionality")
        login('username1', 'password1')
        logged_in1 = is_logged_in()
        print("→ After login: is_logged_in()")
        print(f"← Result: {logged_in1}")
        self.assertTrue(logged_in1)

        logout()
        logged_in2 = is_logged_in()
        print("→ After logout: is_logged_in()")
        print(f"← Result: {logged_in2}")
        self.assertFalse(logged_in2)

    def test_get_current_user(self):
        print("Test Case: get_current_user Functionality")
        login('username1', 'password1')
        user = get_current_user()
        print("→ After login: get_current_user()")
        print(f"← Current user: '{user}'")
        self.assertEqual(user, 'username1')

if __name__ == '__main__':
    print("=== RUNNING LOGIN MODULE TESTS ===")
    unittest.main(verbosity=2)
    print("=== TESTS COMPLETED ===")