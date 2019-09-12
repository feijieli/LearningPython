from flask import Flask, render_template,request,redirect,url_for,flash,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db',connect_args={"check_same_thread": False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id,menu_id):
	item = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem=item.serialize)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/new/',methods=['POST','GET'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',methods=['POST','GET'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        edit_item = session.query(MenuItem).filter_by(id=menu_id).one() 
        edit_item.name=request.form['name']
        session.add(edit_item)
        session.commit()
        flash("Menu item edited!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        edit_item = session.query(MenuItem).filter_by(id=menu_id).one() 
        return render_template('editmenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id, menu_item=edit_item)

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',methods=['POST','GET'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        delete_item = session.query(MenuItem).filter_by(id=menu_id).one() 
        session.delete(delete_item)
        session.commit()
        flash("Menu item deleted!")

        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        delete_item = session.query(MenuItem).filter_by(id=menu_id).one() 
        return render_template('deletemenuitem.html',item=delete_item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)