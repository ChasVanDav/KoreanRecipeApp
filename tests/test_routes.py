import unittest
from app import app
from models import Recipe
from database import SessionLocal

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # setting up Flask app for testing
        cls.client = app.test_client()

        # setting up session for database storage
        cls.session = SessionLocal()

    def tearDown(self):
        """
        Clean up the database after each test to remove any test data
        """
        # to clear the test data from the recipes table after each test
        self.session.query(Recipe).delete()
        self.session.commit()

    def test_home(self):
        # test that the home route renders correctly and returns a status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_video(self):
        # testing for data that is on the homepage
        recipe = Recipe(recipe_title="Budae Jjigae")
        self.session.add(recipe)
        self.session.commit()
        
        response = self.client.get('/video/Budae Jjigae')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Budae Jjigae', response.data.decode())

    def test_edit_video(self):
        recipe = Recipe(recipe_title="Budae Jjigae")
        self.session.add(recipe)
        self.session.commit()

        response = self.client.get(f'/edit_video/{recipe.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Edit Video Title', response.data.decode())

        # to post an update to the video title
        response = self.client.post(f'/edit_video/{recipe.id}', data={'title': 'Army Stew'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')

    @classmethod
    def tearDownClass(cls):
        # to clean up session and database after tests
        cls.session.close()

if __name__ == '__main__':
    unittest.main()



