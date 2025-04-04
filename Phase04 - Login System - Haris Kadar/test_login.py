import unittest
import sqlite3
from login import login, create_user, logout, is_logged_in, get_current_user

class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the database before any tests run
        print("\n=== Setting up test database ===")
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('DELETE FROM users')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")

    def setUp(self):
        # Ensure clean slate for each test
        create_user('user1', 'password1')
        create_user('admin', 'adminpassword')
        print(f"\n--- Starting new test: {self._testMethodName} ---")

    def tearDown(self):
        # Clean up after each test
        logout()
        print(f"--- Finished test: {self._testMethodName} ---")

    def test_login_success(self):
        result1 = login('user1', 'password1')
        print(f"Login with user1/password1: {result1}")
        self.assertTrue(result1)
        
        result2 = login('admin', 'adminpassword')
        print(f"Login with admin/adminpassword: {result2}")
        self.assertTrue(result2)

    def test_login_failure(self):
        result1 = login('user1', 'wrongpassword')
        print(f"Login with user1/wrongpassword: {result1}")
        self.assertFalse(result1)
        
        result2 = login('nonexistent', 'password1')
        print(f"Login with nonexistent/password1: {result2}")
        self.assertFalse(result2)

    def test_create_user_success(self):
        result = create_user('newuser', 'newpassword')
        print(f"Create new user 'newuser': {result}")
        self.assertTrue(result)
        
        login_result = login('newuser', 'newpassword')
        print(f"Login with newuser/newpassword: {login_result}")
        self.assertTrue(login_result)

    def test_create_user_failure(self):
        # User already exists
        result1 = create_user('user1', 'password1')
        print(f"Create duplicate user 'user1': {result1}")
        self.assertFalse(result1)
        
        # Username and password are the same
        result2 = create_user('same', 'same')
        print(f"Create user with username=password='same': {result2}")
        self.assertFalse(result2)

    def test_logout(self):
        login('user1', 'password1')
        print(f"Logged in as user1")
        
        logout_result = logout()
        print(f"Logout result: {logout_result}")
        
        is_logged_in_result = is_logged_in()
        print(f"Is still logged in after logout: {is_logged_in_result}")
        self.assertFalse(is_logged_in_result)

    def test_is_logged_in(self):
        login('user1', 'password1')
        logged_in1 = is_logged_in()
        print(f"Is logged in after login: {logged_in1}")
        self.assertTrue(logged_in1)
        
        logout()
        logged_in2 = is_logged_in()
        print(f"Is logged in after logout: {logged_in2}")
        self.assertFalse(logged_in2)

    def test_get_current_user(self):
        login('user1', 'password1')
        user = get_current_user()
        print(f"Current user after login: '{user}'")
        self.assertEqual(user, 'user1')

if __name__ == '__main__':
    print("=== RUNNING LOGIN MODULE TESTS ===")
    unittest.main(verbosity=2)