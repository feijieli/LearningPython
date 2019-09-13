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
    return 'edit restaurant {}'.format(rest_id)

@app.route('/restaurant/<int:rest_id>/delete')
def DeleteRest(rest_id):
    return 'delete restaurant {}'.format(rest_id)

@app.route('/restaurant/<int:rest_id>/menu')
@app.route('/restaurant/<int:rest_id>')
def VeiwMenus(rest_id):
    return 'menus for restaurant {}'.format(rest_id)


@app.route('/restaurant/<int:rest_id>/menu/new')
def AddMenu(rest_id):
    return 'create a menu for restaurant {}'.format(rest_id)

@app.route('/restaurant/<int:rest_id>/menu/edit')
def EditMenu(rest_id):
    return 'edit a menu for restaurant {}'.format(rest_id)

@app.route('/restaurant/<int:rest_id>/menu/delete')
def DeleteMenu(rest_id):
    return 'delete a menu for restaurant {}'.format(rest_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)