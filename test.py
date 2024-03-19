from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):
    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1> All Users </h1>', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input id="edit-button" type="button"', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.get('/users/form')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a User!</h1>', html)


    def test_new_post(self):
        with app.test_client() as client:
            user = User.query.first()
            data = {'title': 'Test Post', 'content': 'This is a test post.'}
            resp = client.post(f'/users/{user.id}/posts/form', data=data)
            post = Post.query.filter_by(title=data['title']).first()

            self.assertEqual(resp.status_code, 302)
            self.assertIsNotNone(post)

    def test_post_edit_form(self):
        with app.test_client() as client:
            post_id = 1  
            resp = client.get(f'/posts/{post_id}/edit')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Post', resp.data)