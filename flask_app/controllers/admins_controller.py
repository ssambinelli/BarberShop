from flask import Flask, render_template, request, redirect, session
from flask_app import DATABASE
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash
from flask_app.models.admins_model import Admin
from flask_app.models.bookings_model import Booking

# DASHBOARD 
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')


# NEW ADMIN
@app.route('/newadmin')
def new_admin():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_admin.html')


# ADMIN REGISTRATION 
@app.route('/admin/register', methods=['POST'])
def create_user():
    if not Admin.validation(request.form):
        return redirect('/newadmin')
    
    # hashing
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    
    new_user = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_password,
        'confirm_password': hashed_password
    }
    logged_user_id = Admin.create_admin(new_user)
    session['user_id'] = logged_user_id
    return redirect('/dashboard')


@app.route ('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = Admin.get_by_id(data)
    return render_template('dashboard.html', logged_user = logged_user)
    
@app.route('/users/login', methods=['POST'])
def login():
    get_email = {
        'email': request.form['email']
    }
    this_user = Admin.get_user_by_email(get_email)
    
    if not this_user:
        flash("Invalid email or password", "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash("Invalid email or password", "login")
        return redirect('/')
    session['user_id'] = this_user.id
    return redirect('/dashboard')
        
# LOGOUT
@app.route('/logout')
def logout():
    del session['user_id']
    return redirect ('/')

#DISPLAY ALL ADMINS 
@app.route ('/admins')
def admins():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = Admin.get_by_id(data)
    all_admins = Admin.get_all()
    return render_template('admins.html', all_admins = all_admins, logged_user = logged_user)



# EDIT ADMIN -- DISPLAY
@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    one_admin = Admin.get_by_id(data)
    logged_user = Admin.get_by_id({'id':session['user_id']})
    return render_template('edit_admin.html', one_admin=one_admin, logged_user=logged_user)

#EDIT ADMIN -- ACTION
@app.route('/update/<int:id>', methods=['POST']) 
def update(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Admin.valid(request.form):
        return redirect(f'/edit/{id}')
    data ={
        **request.form,
        'id':id
    }
    Admin.edit(data)
    return redirect('/admins')

# DELETE ADMIN 
@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/')
    Admin.delete({'id':id})
    return redirect('/admins')



