from config import create_app, db
from models import Hero, Power, HeroPower

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # HEROES
    h1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
    h2 = Hero(name="Doreen Green", super_name="Squirrel Girl")
    h3 = Hero(name="Gwen Stacy", super_name="Spider-Gwen")
    # add more heroes as needed...

    # POWERS
    p1 = Power(name="super strength", description="gives the wielder super-human strengths")
    p2 = Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed")
    # add more powers...

    # HEROPOWERS
    hp1 = HeroPower(hero=h1, power=p1, strength="Strong")
    hp2 = HeroPower(hero=h3, power=p2, strength="Average")

    db.session.add_all([h1,h2,h3,p1,p2,hp1,hp2])
    db.session.commit()
