from flask import Flask,render_template,request,redirect,url_for,jsonify,flash
from db_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


app=Flask(__name__)



engine = create_engine('sqlite:///restaurantmenu.db',connect_args={"check_same_thread": False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()



@app.route('/restaurants/JSON')
def GetAllRest():
    return jsonify(restaurants=[rest.serialize for rest in session.query(Restaurant).all()])


@app.route('/restaurant/<int:rest_id>/menu/JSON')
def GetMenus(rest_id):
    return jsonify(menus=[menu.serialize for menu in session.query(MenuItem).filter_by(restaurant_id=rest_id).all()])

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/JSON')
def GetMenu(rest_id,menu_id):
    return jsonify(menu= session.query(MenuItem).filter_by(id=menu_id).one().serialize)


@app.route('/')
@app.route('/restaurants')
def ViewAllRest():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html',restaurants = restaurants)

@app.route('/restaurant/new',methods = ['POST','GET'])
def AddRest():
    if request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit() 
        flash("new restaurant created!")
        return redirect(url_for('ViewAllRest'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurant/<int:rest_id>/edit',methods = ['POST','GET'])
def EditRest(rest_id):
    edit_restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        edit_restaurant.name=request.form['name']
        session.add(edit_restaurant)
        session.commit() 
        flash("restaurant edited!")
        return redirect(url_for('ViewAllRest'))
    else:
        return render_template('editrestaurant.html',restaurant = edit_restaurant)    

@app.route('/restaurant/<int:rest_id>/delete',methods = ['POST','GET'])
def DeleteRest(rest_id):
    delete_restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        session.delete(delete_restaurant)
        session.commit() 
        flash("restaurant deleted!")
        return redirect(url_for('ViewAllRest'))
    else:
        return render_template('deleterestaurant.html',restaurant = delete_restaurant)  


@app.route('/restaurant/<int:rest_id>/menu')
@app.route('/restaurant/<int:rest_id>')
def ViewMenus(rest_id):
    menu_items = session.query(MenuItem).filter_by(restaurant_id = rest_id).all()
    return render_template('menu.html',rest_id=rest_id,menuitems=menu_items)


@app.route('/restaurant/<int:rest_id>/menu/new',methods = ['POST','GET'])
def AddMenu(rest_id):
    if request.method == 'POST':
        new_menu_item = MenuItem(name=request.form['name'],restaurant_id = rest_id)
        session.add(new_menu_item)
        session.commit() 
        return redirect(url_for('ViewMenus',rest_id = rest_id))
    else:
        return render_template('newmenuitem.html',rest_id = rest_id)

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/edit',methods = ['POST','GET'])
def EditMenu(rest_id,menu_id):
    edit_menu = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        edit_menu.name=request.form['name']
        session.add(edit_menu)
        session.commit() 
        return redirect(url_for('ViewMenus',rest_id=rest_id))
    else:
        return render_template('editmenuitem.html',menuitem = edit_menu)   

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/delete',methods = ['POST','GET'])
def DeleteMenu(rest_id,menu_id):
    delete_menu = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(delete_menu)
        session.commit() 
        return redirect(url_for('ViewMenus',rest_id=rest_id))
    else:
        return render_template('deletemenuitem.html',menuitem = delete_menu)  


if __name__ == '__main__':
    app.secret_key = 'super secret'
    app.debug = True
    app.run(host='0.0.0.0',port=5000)