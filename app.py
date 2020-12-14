from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bea.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    url = db.Column(db.String(255))

    def __repr__(self):
        return '<Restaurant %s>' % self.title


class RestaurantSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "url")


restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)


class RestaurantListResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return restaurants_schema.dump(restaurants)


class RestaurantResource(Resource):
    def get(self, restaurant_id):
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        return restaurant_schema.dump(restaurant)


api.add_resource(RestaurantListResource, '/restaurants')
api.add_resource(RestaurantResource, '/restaurant/<int:restaurant_id>')


if __name__ == '__main__':
    app.run(debug=True)
