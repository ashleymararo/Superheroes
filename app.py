from flask import request
from config import create_app, db
from models import Hero, Power, HeroPower

app = create_app()

# HERO ROUTES
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return [hero.to_dict(only=('id','name','super_name')) for hero in heroes], 200

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return {"error":"Hero not found"}, 404
    return hero.to_dict(), 200

# POWER ROUTES
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return [power.to_dict() for power in powers], 200

@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return {"error":"Power not found"}, 404
    return power.to_dict(), 200

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return {"error":"Power not found"}, 404
    try:
        data = request.json
        power.description = data.get('description')
        db.session.commit()
        return power.to_dict(), 200
    except ValueError:
        return {"errors":["validation errors"]}, 400

# HEROPOWER ROUTE
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    try:
        hero = Hero.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])
        if not hero or not power:
            raise ValueError
        hero_power = HeroPower(strength=data['strength'], hero=hero, power=power)
        db.session.add(hero_power)
        db.session.commit()
        return hero_power.to_dict(), 201
    except:
        return {"errors":["validation errors"]}, 400

if __name__ == '__main__':
    app.run(debug=True)
