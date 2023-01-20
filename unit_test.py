import os
os.environ['DATABASE_URL'] = 'sqlite://'

from app import app, db
from app.models import User, Post
from datetime import datetime, timedelta
import unittest



class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='Pepe')
        u.set_password('Frog')
        self.assertFalse(u.check_password('Fly'))
        self.assertTrue(u.check_password('Frog'))

    def test_avatar(self):
        u = User(username='Sano', email='Sano@sok4e.com')
        self.assertEqual(u.avatar(128), 
        ('https://www.gravatar.com/avatar/c135f1083aa298fc1b95c11ffce4984e?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username = 'Pepe', email = 'Pepe@frog.com')
        u2 = User(username = 'Sano', email = 'Sano@sok4e.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'Sano')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'Pepe')

    def test_follow_posts(self):
        # users
        u1 = User(username = 'Pepe', email = 'Pepe@frog.com')
        u2 = User(username = 'Sano', email = 'Sano@sok4e.com')
        u3 = User(username = 'Grog', email = 'Grog@frog.com')
        u4 = User(username = 'Boby', email = 'Bob@bro.com')
        db.session.add_all([u1, u2, u3, u4])

        # user's posts
        now = datetime.utcnow()
        p1 = Post(body='Post from Pepe', author = u1,
                timestamp=now + timedelta(seconds=1))
        p2 = Post(body='Post from Sano', author = u2,
                timestamp=now + timedelta(seconds=4))
        p3 = Post(body='Post from Grog', author = u3,
                timestamp=now + timedelta(seconds=3))
        p4 = Post(body='Post from Boby', author = u4,
                timestamp=now + timedelta(seconds=2))        
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # followers
        u1.follow(u2) # Pepe follows Sano
        u1.follow(u4) # Pepe follows Boby
        u2.follow(u3) # Sano follows Grog
        u3.follow(u4) # Grog follows Boby
        db.session.commit()

        # users view
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1]) # Pepe's view
        self.assertEqual(f2, [p2, p3]) # Sano's view
        self.assertEqual(f3, [p3, p4]) # Grog's view 
        self.assertEqual(f4, [p4])  # Boby's view :'(

if __name__ == '__main__':
    unittest.main(verbosity = 2)

