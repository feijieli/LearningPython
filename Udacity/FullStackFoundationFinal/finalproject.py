from flask import Flask,render_template


app=Flask(__name__)


restaurant = {'name' : 'rest1','id':1}
restaurants = [{'name' : 'rest1','id':1},{'name' : 'rest2','id':2}]

menu_item = {'name':'item1', 'id' : 1}
menu_items = [{'name':'item1', 'id' : 1},{'name':'item2', 'id' : 2}]


@app.route('/')
@app.route('/restaurants')
def ViewAllRest():
    return render_template('restaurants.html',restaurants = restaurants)

@app.route('/restaurant/new')
def AddNewRest():
    return render_template('newrestaurant.html')

@app.route('/restaurant/<int:rest_id>/edit')
def EditRest(rest_id):
    return render_template('editrestaurant.html',restaurant = restaurant)

@app.route('/restaurant/<int:rest_id>/delete')
def DeleteRest(rest_id):
    return render_template('deleterestaurant.html',restaurant = restaurant)


@app.route('/restaurant/<int:rest_id>/menu')
@app.route('/restaurant/<int:rest_id>')
def VeiwMenus(rest_id):
    return render_template('menu.html',rest_id=rest_id,menuitems=menu_items)


@app.route('/restaurant/<int:rest_id>/menu/new')
def AddMenu(rest_id):
    return render_template('newmenuitem.html')

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/edit')
def EditMenu(rest_id,menu_id):
    return render_template('editmenuitem.html',menuitem=menu_item)

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/delete')
def DeleteMenu(rest_id,menu_id):
    return render_template('deletemenuitem.html',menuitem = menu_item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)