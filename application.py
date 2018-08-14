from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from flask import session as login_session, make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from model import Base, Category, CategoryItem, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random
import string
import httplib2
import json
import requests
import uuid

app = Flask(__name__)

app.secret_key = '081418' 
app.debug = True

# Setup the client secrets needed for Google OAuth Login
# Per readme this must be in place for application to run
CLIENT_ID = json.loads(
    open('/var/www/html/catalog/client_secrets.json', 'r').read())['web']['client_id']

# Setup the catalog database and create session for query/updates
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/categories/')
def showCategories():
    """
    This route is like showCategory but displays recent items.
    """
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(
        CategoryItem).order_by(CategoryItem.id.desc()).limit(10)
    return render_template('home.html', categories=categories, items=items)


@app.route('/categories/<string:category_name>/items/<int:category_id>/')
def showCategory(category_name, category_id):
    """
    Route shows category with items. The home route shows recent.
    Could combine the template in future to minimize code
    """
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()
    return render_template('viewcategory.html', categories=categories,
                           category=category, items=items)


@app.route(
    '/categories/<string:category_name>/item/ \
    <string:item_name>/<int:category_item_id>/')
def viewCategoryItem(category_name, item_name, category_item_id):
    """
    This route will view an item. Note named not used
    but in URL for SEO purposes
    """
    categoryItem = session.query(CategoryItem).filter_by(
        id=category_item_id).one()
    return render_template('viewItem.html', category_item=categoryItem)


@app.route('/item/<int:category_id>/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    """
    This route will take entry details for new item and store
    in database redirecing to category page for POST or display
    the new item html page on GET
    """
    if 'username' not in login_session:
        print ('user not in session')
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()

    # TODO: Future option to check category owners, not implemented yet
    # if login_session['user_id'] != category.user_id:
    #    return render_template('securityerror.html',
    #    message = "You're not authorized to edit this item!")

    if request.method == 'POST':
        print ("post")
        new_item = CategoryItem(name=request.form['name'],
                                description=request.form['description'],
                                price=request.form['price'],
                                category_id=category_id,
                                user_id=login_session['user_id'])
        session.add(new_item)
        session.commit()
        flash('New Item %s Successfully Created' % (new_item.name))
        return redirect(url_for('viewCategoryItem',
                                category_name=new_item.category.name,
                                item_name=new_item.name,
                                category_item_id=new_item.id))
    else:
        categories = session.query(Category).order_by(asc(Category.name))
        return render_template('newitem.html',
                               categories=categories,
                               category=category)


@app.route('/item/<int:category_item_id>/edit', methods=['GET', 'POST'])
def editCategoryItem(category_item_id):
    """
    This route lets you edit and item. checks ID on item for
    user in session. After editing (POST) goes to the view
    item route.
    """
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(
        CategoryItem).filter_by(id=category_item_id).one()
    categories = session.query(Category).order_by(asc(Category.name))
    if login_session['user_id'] != editedItem.user_id:
        return render_template('securityerror.html',
                               message="You're not authorized to edit item!")
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['category']:
            editedItem.category_id = request.form['category']
        session.add(editedItem)
        session.commit()
        flash('Item Changes Saved')
        return redirect(url_for('viewCategoryItem',
                                category_name=editedItem.category.name,
                                item_name=editedItem.name,
                                category_item_id=editedItem.id))
    else:
        return render_template('edititem.html', item=editedItem,
                               categories=categories)


@app.route('/item/<int:category_item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_item_id):
    """
    This route takes the item ID and deletes on POST and
    redirects to category page or sets up delete page
    on GET
    """
    if 'username' not in login_session:
        return redirect('/login')
    item_to_delete = session.query(
        CategoryItem).filter_by(id=category_item_id).one()
    if login_session['user_id'] != item_to_delete.user_id:
        return render_template('securityerror.html',
                               message="You're not authorized to delete item!")
    if request.method == 'POST':
        category_name = item_to_delete.category.name
        category_id = item_to_delete.category.id
        session.delete(item_to_delete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showCategory',
                                category_name=category_name,
                                category_id=category_id))
    else:
        return render_template('deleteitem.html', item=item_to_delete)


@app.route('/api/v1/categories')
def categoriesJSON():
    """
    JSON view of all the categories,
    other JSON endpoint can be used for items
    """
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


@app.route('/api/v1/categories/<int:category_id>/items')
def categoryItemsJSON(category_id):
    """ JSON view of all items in a category by ID """
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])


@app.route('/api/v1/items/<int:item_id>')
def itemJSON(item_id):
    """
    JSON view of a single item.
    Not useful IMHO but required for project spec
    """
    items = session.query(CategoryItem).filter_by(id=item_id).one()
    return jsonify(CategoryItems=items.serialize)


@app.route('/login')
def showLogin():
    """
    Create state token and send user to the login page for Google login
    If user completes login the /gconnect route is invoked.
    """
    state = str(uuid.uuid4()).replace('-', '')
    login_session['state'] = state
    return render_template('login.html', STATE=state, ID=CLIENT_ID)


@app.route('/gconnect', methods=['POST', 'GET'])
def gconnect():
    """
    Callback to process the Google Login.
    The basic flow is to take the code and use
    it to get a token from Google we can use to get user details.
    After that we'll load it in the http session and create the user if new
    """
    # Validate same GUID as when routed to login page
    print(login_session['state'])
    print(request.args.get('state'))
    if request.args.get('state') != login_session['state']:
        return render_template('securityerror.html',
                               message="Invalid State, Logout failed")

    # Get the auth code from request to exchange for credentials
    code = request.args.get('code')
    print("code:" + code)
    try:
        # Upgrade  auth code to credentials object
        # These lines of code based on examples from class
        oauth_flow = flow_from_clientsecrets('/var/www/html/catalog/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:
        return render_template('securityerror.html',
                               message="Problem with auth code")

    # Validate access token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    print(result)    

    # If response has error display to user
    if result.get('error') is not None:
        return render_template('securityerror.html',
                               message=result.get('error'))

    # check token matches user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return render_template('securityerror.html',
                               message="Token ID does not make user ID")

    # Check matches app by client ID
    if result['issued_to'] != CLIENT_ID:
        return render_template('securityerror.html',
                               message="Token ID isn't for this app")

    # Store the access token
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Call Google to get user information
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    print(userinfo_url)
    print(params)
    answer = requests.get(userinfo_url, params=params)
    print(answer)
    print(answer.text)
    data = answer.json

    # Store results in session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Create user if needed
    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    # redirect user with message
    flash("Logged in as : %s" % login_session['username'])
    return redirect(url_for('showCategories'))


def create_user(login_session):
    """
    Grab user details from session and add to database. Put new ID in session
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_id(email):
    """
    Get the userid number based on email DB query
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/disconnect')
def disconnect():
    """
    Logout user from google perspective (called by logout)
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        return render_template('securityerror.html',
                               message="Cannot logout, user not connected")
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # Log message, but proceed with logout
    if result['status'] != '200':
        print('Failed to revoke token for given user.')

    # Clean up session
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    flash("You have been logged out")
    return redirect(url_for('showCategories'))

if __name__ == '__main__':
    # UUID for app secret means sessions new after reloader runs since unique
    # Change this to static value and debug before production use
    app.secret_key = str(uuid.uuid4()).replace('-', '')

    app.debug = False
    #app.run(host='172.26.9.18', port=80)
    app.run()
