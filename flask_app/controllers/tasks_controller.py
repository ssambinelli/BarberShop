from flask import Flask, render_template, request, redirect, session
from flask_app import DATABASE
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash
from flask_app.models.admins_model import Admin
from flask_app.models.bookings_model import Booking


# TO DO LIST 
@app.route('/todolist')
def to_do_list():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('todolist.html')

# SETTINGS
@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('settings.html')

# CALENDAR
@app.route('/calendar')
def calendar():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('calendar.html')

# BOOKING AN APPOIMENT -- DISPLAY 
@app.route('/booktime')
def booktime():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('bookings.html')

# BOOKING AN APPOIMENT -- ACTION 
@app.route('/newbooking', methods=['POST'])
def book_appt():
    if 'user_id' not in session:
        return redirect('/')
    if not Booking.validation(request.form):
        return redirect('/booktime')
    
    new_appt = {
        'client_name': request.form['client_name'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'date': request.form['date'],
        'time': request.form['time'],
        'service': request.form['service'],
    }
    Booking.new_appt(new_appt)
    return redirect('/calendar')

# EDIT AN APPOITMENT -- DISPLAY
@app.route('/editbooking/<int:id>')
def edit_appt(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    one_appt = Booking.get_by_id(data)
    # logged_user = Admin.get_by_id({'id':session['user_id']})
    return render_template('edit_admin.html', one_appt=one_appt) #logged_user=logged_user)

# EDIT THE APPOITMENT -- ACTION
@app.route('/updateappt')
def update_appt():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('bookings_edit.html')


# DELETE AN APPOITMENT 
@app.route('/cancel/<int:id>')
def cancel(id):
    if 'user_id' not in session:
        return redirect('/')
    Booking.delete({'id':id})
    return redirect('/calendar')

