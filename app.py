from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_mysqldb import MySQL
from forms import BookingForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'robin12mysql'
app.config['MYSQL_DB'] = 'hotel_reservation'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        admin = cur.fetchone()
        cur.close()

        if admin:
            session['admin_logged_in'] = True
            session['admin_username'] = admin[1]
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid login credentials', 'danger')

    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    form = BookingForm()

    room_from_url = request.args.get('room')
    if room_from_url and not form.room_type.data:
        form.room_type.data = room_from_url

    if form.validate_on_submit():
        room_type = form.room_type.data
        check_in = form.check_in.data
        check_out = form.check_out.data
        guest_name = form.guest_name.data
        adults = form.adults.data
        children = form.children.data

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM room WHERE room_type = %s", (room_type,))
        room = cur.fetchone()

        if not room or room[4] < 1:
            flash('Selected room type is not available right now.', 'danger')
            return redirect(url_for('book'))

        nights = (check_out - check_in).days
        if nights <= 0:
            flash('Invalid check-in/check-out dates.', 'warning')
            return redirect(url_for('book'))

        total_price = nights * room[2]

        cur.execute("""
            INSERT INTO booking 
            (guest_name, room_type, check_in, check_out, adults, children, nights, total_price) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (guest_name, room_type, check_in, check_out, adults, children, nights, total_price))

        cur.execute("UPDATE room SET available_rooms = available_rooms - 1 WHERE room_type = %s", (room_type,))
        mysql.connection.commit()
        cur.close()

        booking = {
            'guest_name': guest_name,
            'room_type': room_type,
            'check_in': check_in,
            'check_out': check_out,
            'adults': adults,
            'children': children,
            'nights': nights,
            'total_price': total_price
        }
        return render_template('success.html', booking=booking)

    return render_template('book.html', form=form)

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash("Unauthorized access. Please login as admin.", 'warning')
        return redirect(url_for('admin_login'))

    cur = mysql.connection.cursor()

    # Fetch rooms
    cur.execute("SELECT * FROM room")
    rooms = cur.fetchall()

    # Fetch bookings
    cur.execute("SELECT * FROM booking ORDER BY check_in DESC")
    bookings = cur.fetchall()

    # Fetch reviews
    cur.execute("SELECT * FROM reviews ORDER BY submitted_at DESC")
    reviews = cur.fetchall()

    cur.close()
    return render_template('admin_dashboard.html', rooms=rooms, bookings=bookings, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)

