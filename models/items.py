from flask import render_template, request, redirect, \
    url_for, flash
from sqlalchemy import asc
from database_setup import Shop, Item
from flask import session as login_session
from functools import wraps
from user import *


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        else:
            return func(*args, **kwargs)
    return wrapper


def exiting_required(func):
    # user input shop_id and item_id must be valid
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return redirect('/')
    return wrapper


# Show the main page
@app.route('/')
def showPortfoliopage():
    return render_template('index.html')


@app.route('/home/')
def showHomepage():
    if 'username' not in login_session:
        return render_template('/home.html')
    else:
        user_id = login_session['user_id']
        user = session.query(User).filter_by(id=user_id).one()
        return render_template('home.html', user_name=user.name)


# Show all shops
@app.route('/shops/')
def showShops():
    shops = session.query(Shop, User).order_by(asc(Shop.name))
    if 'username' not in login_session:
        return render_template('publicshops.html', shops=shops, )
    else:
        return render_template('shops.html', shops=shops,)


def validShopname(name):
    # shop name must be unique
    try:
        existingShop = session.query(Shop).filter_by(name=name).one()
        if existingShop:
            return False
    except:
        return True


# Create a new shop
@app.route('/shop/new/', methods=['GET', 'POST'])
@login_required
def newShop():
    if request.method == 'POST':
        name = request.form['name']
        if validShopname(name):
            user_id = login_session['user_id']
            newShop = Shop(name=name, user_id=user_id)
            session.add(newShop)
            flash('New Shop %s Successfully Created' % newShop.name)
            session.commit()
        else:
            flash('Name %s has been used.Please try another one.' % name,
                  'error')
        return redirect(url_for('showShops'))
    else:
        return render_template('newShop.html')


# Edit a shop
@app.route('/shop/<int:shop_id>/edit/', methods=['GET', 'POST'])
@exiting_required
@login_required
def editShop(shop_id):
    editedShop = session.query(Shop).filter_by(id=shop_id).one()
    if editedShop.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not  " \
               "authorized.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        name = request.form['name']
        if validShopname(name):
            editedShop.name = name
            flash('Shop Successfully Edited %s' % editedShop.name)
        else:
            flash('Name %s has been used.Please try another one.' % name,
                  'error')
        return redirect(url_for('showShops'))
    else:
        return render_template('editShop.html', shop=editedShop)


# Delete a shop
@app.route('/shop/<int:shop_id>/delete/', methods=['GET', 'POST'])
@exiting_required
@login_required
def deleteShop(shop_id):
    shopToDelete = session.query(
        Shop).filter_by(id=shop_id).one()
    if shopToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not  " \
               "authorized. ');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(shopToDelete)
        flash('%s Successfully Deleted' % shopToDelete.name)
        session.commit()
        return redirect(url_for('showShops', shop_id=shop_id))
    else:
        return render_template('deleteShop.html', shop=shopToDelete)

# Show a category item
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item/')
@exiting_required
def showCategoryItem(category_id):
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return render_template('publiccategory.html', items=items)




# Show a shop item
@app.route('/shop/<int:shop_id>/')
@app.route('/shop/<int:shop_id>/item/')
@exiting_required
def showItem(shop_id):
    shop = session.query(Shop).filter_by(id=shop_id).one()
    creator = getUserInfo(shop.user_id)
    items = session.query(Item).filter_by(
        shop_id=shop_id).all()
    if 'username' not in login_session or creator.id != login_session[
        'user_id']:
        return render_template('publicitem.html', items=items, shop=shop,
                               creator=creator)
    else:
        return render_template('item.html', items=items, shop=shop,
                               creator=creator)


# Create a new item
@app.route('/shop/<int:shop_id>/item/new/', methods=['GET', 'POST'])
@exiting_required
@login_required
def newItem(shop_id):
    shop = session.query(Shop).filter_by(id=shop_id).one()
    if login_session['user_id'] != shop.user_id:
        return "<script>function myFunction() {alert('You are not  " \
               "authorized.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       price=request.form[
                           'price'], category_id=request.form['category_id'], shop_id=shop_id, user_id=shop.user_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showItem', shop_id=shop_id))
    else:
        return render_template('newitem.html', shop_id=shop_id)


# Edit an item
@app.route('/shop/<int:shop_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
# @exiting_required
@login_required
def editItem(shop_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    shop = session.query(Shop).filter_by(id=shop_id).one()
    if login_session['user_id'] != shop.user_id:
        return "<script>function myFunction() {alert('You are not  " \
               "authorized.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['category_id']:
            editedItem.category_id = request.form['category_id']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showItem', shop_id=shop_id))
    else:
        return render_template('edititem.html', shop_id=shop_id,
                               item_id=item_id, item=editedItem)


# Delete an item
@app.route('/shop/<int:shop_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
@exiting_required
@login_required
def deleteItem(shop_id, item_id):
    shop = session.query(Shop).filter_by(id=shop_id).one()
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if login_session['user_id'] != shop.user_id:
        return "<script>function myFunction() {alert('You are not  " \
               "authorized. ' " \
               " );}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showItem', shop_id=shop_id))
    else:
        return render_template('deleteitem.html', item=itemToDelete,
                               shop_id=shop_id)
