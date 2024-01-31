# Application: Blogly
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

def create_app():
    DATABASE_URL = 'postgresql:///blogly_users_db'
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG'] = True
    
    connect_db(app)
    
    return app

app = create_app()

@app.route('/')
def home_page():
    """shows list of users"""
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Shows verbose info for selected user"""
    user = User.query.filter_by(id=user_id).first()
    return render_template('detail.html', user=user)

@app.route('/users/new', methods=['GET'])
def show_create_users_form():
    """shows new user creation form"""
    return render_template('create_user.html')
    
@app.route('/users/new', methods=['POST'])
def process_create_users_form():
    """process user creation form"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = str(image_url) if image_url else "/static/default_icon.png"
    print(f"first name: {first_name} | last name: {last_name} | image_url: {image_url}")
    add_user(first_name, last_name, image_url)
    return redirect('/')

@app.route('/users/<int:user_id>/delete')
def show_confirm_delete_page(user_id):
    """show user deletion confirmation form"""
    return render_template('delete_user_confirmation.html', user=User.query.filter_by(id=user_id).first())

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def confirmed_remove_user(user_id):
    """deletes user and redirects to / page"""
    del_user(user_id)
    return redirect('/')

@app.route('/users/<int:user_id>/edit')
def show_edit_user_page(user_id):
    """shows user edit page"""
    user = User.query.filter_by(id=user_id).first()
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def confirmed_edit_user(user_id):
    """confirm users edit page and redirects to edited suer"""
    first_name = request.form['first_name']
    first_name = first_name if first_name else None

    last_name = request.form['last_name']
    last_name = last_name if last_name else None

    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    user = User.query.filter_by(id=user_id).first()
    
    edit_user(user, first_name, last_name, image_url)
    
    return redirect(f'/users/{user_id}') # redirect to edited user to show new information

def add_user(first_name, last_name, image_url):
    """Logic function adding user to db"""
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

def del_user(user_id):
    """Logic function deleting user to db"""
    User.query.filter_by(id=user_id).delete() # should delete
    print(f'removed user {user_id}')
    db.session.commit()
    

def edit_user(user, first_name=None, last_name=None, image_url=None):
    """Logic function editing user to db"""
    if first_name != None:
        user.first_name = first_name
    if last_name != None:
        user.last_name = last_name
    if image_url != None:
        user.image_url = image_url
    
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)