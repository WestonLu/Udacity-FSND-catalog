from flask import jsonify
from database_setup import Base, Shop, Item, User, Category
from flaskfile import app, session


# JSON APIs to view Shop Information
@app.route('/shop/<int:shop_id>/item/JSON')
def shopItemJSON(shop_id):
    items = session.query(Item).filter_by(
        shop_id=shop_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/shop/JSON')
def shopsJSON():
    shops = session.query(Shop).all()
    return jsonify(shops=[r.serialize for r in shops])

@app.route('/item/JSON')
def itemJSON():
    items = session.query(Item).all()
    return jsonify(Items=[r.serialize for r in items])

@app.route('/category/JSON')
def categoryJSON():
    items = session.query(Category).all()
    return jsonify(Category=[r.serialize for r in items])