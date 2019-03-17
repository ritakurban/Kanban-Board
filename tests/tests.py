import os
import unittest
import sys
import requests
# Find path to the directory above the file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from kanban import app, db


TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):
    '''
    Execute prior to each test.
    '''
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    '''
    Execute after each test
    '''
    def tearDown(self):
        pass

# Tests

    def test_main_page(self):
        '''
        Test that the main page is loaded successfully.
        '''
        req = self.app.get('/main', follow_redirects=True)
        self.assertEqual(req.status_code, 200)

    def test_login(self):
        '''
        Test that the app shows the login page if the user is not logged in.
        '''
        req = requests.get('http://127.0.0.1:5000/')
        self.assertEqual(req.url, 'http://127.0.0.1:5000/login')

    def test_registration(self):
        '''
        Test that registration succeeds and a registered user can get to the main page.
        '''
        details = {'username':'Dolly', 'password':'ncelekckln!mv', 'repeat':'ncelekckln!mv'}
        req = requests.post('http://127.0.0.1:5000/register', data = details)
        req = requests.post('http://127.0.0.1:5000/login', data = details)
        self.assertEqual(req.url, 'http://127.0.0.1:5000/main')


    def test_right_login(self):
        '''
        Test that users with correct credentials can access their board.
        '''
        details = {'username':'Dolly',  'password':'ncelekckln!mv'}
        req = requests.post('http://127.0.0.1:5000/login', data = details)

        self.assertEqual(req.url, 'http://127.0.0.1:5000/main')

    def test_faulty_login(self):
        '''
        Test that users with incorrect credentials remain on login page.
        '''
        details = {'username':'Rita', 'password':'fake'}
        req = requests.post('http://127.0.0.1:5000/login', data = details)

        self.assertEqual(req.url, 'http://127.0.0.1:5000/login')




if __name__ == "__main__":
    unittest.main()
