from sqlalchemy.exc import IntegrityError
import pytest

from app import app
from models import db, User, Recipe

class TestUser:
    '''User in models.py'''

    def test_has_attributes(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(
                username="Liz",
                image_url="https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg",
                bio="Dame Elizabeth Rosemond Taylor DBE (February 27, 1932 - March 23, 2011) ..."
            )
            user.password = "whosafraidofvirginiawoolf"

            db.session.add(user)
            db.session.commit()

            created_user = User.query.filter_by(username="Liz").first()

            assert created_user.username == "Liz"
            assert created_user.image_url == "https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg"
            assert created_user.bio == "Dame Elizabeth Rosemond Taylor DBE (February 27, 1932 - March 23, 2011) ..."

            with pytest.raises(AttributeError):
                created_user.password_hash

    def test_requires_username(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User()
            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()

        def test_requires_unique_username(self):
            '''requires each record to have a username.'''

            with app.app_context():

                User.query.delete()
                db.session.commit()

                user_1 = User(username="Ben")
                user_2 = User(username="Ben")

                with pytest.raises(IntegrityError):
                    db.session.add_all([user_1, user_2])
                    db.session.commit()

    def test_has_list_of_recipes(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()

            user = User(username="Prabhdip")
            user.password = "example_password" 
            db.session.add(user)
            db.session.commit()

            recipe_1 = Recipe(
                user_id=user.id,
                title="Delicious Shed Ham",
                instructions="Or kind rest bred with am shed then. Here are the detailed instructions to make this delicious dish.",
                minutes_to_complete=60,
            )
            recipe_2 = Recipe(
                user_id=user.id,
                title="Another Recipe",
                instructions="Here is another set of detailed instructions for a different recipe that meets the 50 character requirement.",
                minutes_to_complete=30,
            )
            db.session.add_all([recipe_1, recipe_2])
            db.session.commit()

            assert len(user.recipes) == 2
            assert user.recipes[0].title == "Delicious Shed Ham"
            assert user.recipes[1].title == "Another Recipe"