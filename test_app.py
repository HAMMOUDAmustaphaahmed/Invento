import unittest
from app import app, db  # Import your Flask app and database

class BasicTests(unittest.TestCase):

    # Runs before each test
    def setUp(self):
        # Setup the test client
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Setup a clean database before each test
        db.create_all()

    # Runs after each test
    def tearDown(self):
        # Clean up the database after each test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Example test: Test if the home route returns a 200 OK status
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    # Example test: Testing the `/confirm_vente` route (POST request)
    def test_confirm_vente(self):
        response = self.app.post('/confirm_vente/1')
        self.assertEqual(response.status_code, 200)
        # You can also check the response data for specific content
        # self.assertIn(b'Success', response.data)
        # Test if the `/achats` route returns a 200 OK status
    def test_achats_page(self):
        response = self.app.get('/achats')
        self.assertEqual(response.status_code, 200)

    # Test if the `/ventes` route returns a 200 OK status
    def test_ventes_page(self):
        response = self.app.get('/ventes')
        self.assertEqual(response.status_code, 200)
        # Test if the search article route works (POST request)
    def test_search_article(self):
        response = self.app.post('/search_article', data={'query': 'article1'})
        self.assertEqual(response.status_code, 200)
        # Vérifier si un article spécifique est retourné dans la réponse
        self.assertIn(b'article1', response.data)
        # Test if the `/add_article` route works (POST request)
    def test_add_article(self):
        new_article = {
            'code_article': 'ART001',
            'libelle_article': 'Nouveau Article',
            'quantite': 10,
            'prix_achat': 15.5
        }
        response = self.app.post('/add_article', data=new_article)
        self.assertEqual(response.status_code, 200)
        # Vérifie si l'article est ajouté avec succès (par exemple, une chaîne de confirmation dans la réponse)
        self.assertIn('Article ajouté avec succès', response.data)

            # Test if the `/edit_article/<id>` route works (POST request)
    def test_edit_article(self):
        updated_article = {
            'libelle_article': 'Article Modifié',
            'quantite': 20,
            'prix_achat': 25.0
        }
        response = self.app.post('/edit_article/1', data=updated_article)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Article mis à jour avec succès', response.data)

            # Test if the `/delete_article/<id>` route works
    def test_delete_article(self):
        response = self.app.post('/delete_article/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Article supprimé avec succès', response.data)

        # Test if the `/analytics` route returns a 200 OK status
    def test_analytics_page(self):
        response = self.app.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'KPI', response.data)

        # Test if the `/approve_achat/<id>` route works
    def test_approve_achat(self):
        response = self.app.post('/approve_achat/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Achat approuvé avec succès', response.data)

    # Test if the `/approve_vente/<id>` route works
    def test_approve_vente(self):
        response = self.app.post('/approve_vente/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Vente approuvée avec succès', response.data)


if __name__ == "__main__":
    unittest.main()
