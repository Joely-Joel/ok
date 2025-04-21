from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db_path = r'\\newcollege.ac.uk\documents\ExamData\PDD741124\Downloads\SQLiteDatabaseBrowserPortable\book.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # PK is always unique
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)


class MessageTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # PK is always unique
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    message = db.Column(db.String(), nullable=False)


class BookingTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False)  # YYYY-MM-DD format
    time = db.Column(db.String(), nullable=False)  # HH:MM format

    def __repr__(self):
        return f"<Booking {self.name} on {self.date} at {self.time}>"


# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')


# Route for the sign-up or login page
@app.route('/sign', methods=['Get', 'POST'])
def sign():
    if request.method == 'POST':
        Username = request.form['username']
        Password = request.form['password']
        try:
            Email = request.form['email']
        except:
            Email = ""
        else:
            Email = request.form['email']

        if Email != "":
            Record = UserTable(username=Username, password=Password, email=Email)
            db.session.add(Record)
            db.session.commit()
            return redirect('/sign')
        else:
            CurrentUser = UserTable.query.filter_by(username=Username).first()
            if CurrentUser.password == Password:
                return redirect('/user')

    return render_template('sign.html')


@app.route('/solar', methods=['GET', 'POST'])
def solar():
    if request.method == 'POST':
        # Capture the form data
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']

        # Check if all fields are filled
        if not name or not date or not time:
            return "Please fill in all fields"

        print(f"Received booking data - Name: {name}, Date: {date}, Time: {time}")

        try:
            # Create a new booking record
            booking_table = BookingTable(name=name, date=date, time=time)
            db.session.add(booking_table)
            db.session.commit()  # Commit the transaction to the database

            # Show confirmation after the booking is saved
            return render_template('confirmation.html', name=name, date=date, time=time)
        except Exception as e:
            print(f"Error saving booking: {e}")
            return "An error occurred while saving the booking"

    return render_template('solar.html')  # Booking form template


# Route for the blog page
@app.route('/educational')
def educational():
    return render_template('educational.html')


# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')


# Route for the shop page
@app.route('/service')
def service():
    return render_template('service.html')


# Route for the contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Route for the products page
@app.route('/products')
def products():
    return render_template('products.html')


# Route for the consultation page
@app.route('/consultation')
def consultation():
    return render_template('consultation.html')


# Route for the consultation page
@app.route('/installation')
def installation():
    return render_template('installation.html')


# Route for the carbon-footprint page
@app.route('/carbon')
def carbon():
    return render_template('carbon.html')


# Route for the energy page
@app.route('/energy')
def energy():
    return render_template('energy.html')


# Route for the FAQ page
@app.route('/faq')
def faq():
    return render_template('faq.html')


# Route to handle form submissions from the contact page
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        print(f"Message from {name} ({email}): {message}")

        # Assuming you have a MessageTable to store the messages
        record = MessageTable(name=name, email=email, message=message)
        db.session.add(record)
        db.session.commit()

        return redirect('/submit')

    return render_template('submit.html')


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/ev')
def ev():
    return render_template('ev.html')


@app.route('/house')
def house():
    return render_template('house.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures all tables are created

    app.run(debug=True)


