from flask import Flask, render_template, request, redirect,url_for, session,jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
#from flask import razorpay


app = Flask(__name__)
app.secret_key = "1aBcD3eFgH5iJkL7mN9oPqR0sTuV2wXyZ"

# # Initialize Razorpay client with your API keys
# razorpay_client = razorpay.Client(auth=("rzp_test_GBeaO6CKSUvIH3", "Bsd6uxJiDqk8oMYhGzUmGNDg"))

# @app.route('/payment', methods=['POST'])
# def initiate_payment():
#     amount = 50000  # Amount in paise (i.e., ₹500)
#     currency = 'INR'

#     # Create a Razorpay order
#     order = razorpay_client.order.create({'amount': amount, 'currency': currency})

#     return jsonify(order)


# MySQL Configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pass@123'
app.config['MYSQL_DB'] = 'milk_order_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

#User Loader Function
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(UserMixin):
        def __init__(self, user_id, name, email):
            self.id = user_id
            self.name = name
            self.email = email

        @staticmethod
        def get(user_id)    :
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT name, email FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return User(user_id, result['name'], result['email'])
            
# Route to render the login page
@app.route('/loginpage', methods = ['GET','POST'])
def showloginpage():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and bcrypt.check_password_hash(user_data['password'],password):
            user = User(user_data['id'],user_data['name'],user_data['email'])
            login_user(user)
            return redirect (url_for('showhomepage'))


    return render_template('login.html')




# Route to render the registration page
@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor = mysql.connection.cursor()

        cursor.execute('INSERT INTO users (name, email, password) VALUES (%s,%s,%s)', (name,email,hashed_password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('showloginpage'))

        
    return render_template('register.html')


# Route to render the index page
@app.route('/')
def showindexpage():
    
    return render_template('index.html')

# Route to render the home page
@app.route('/home')
def showhomepage():
    
    return render_template('home.html')


# Route to render the milk order form
@app.route('/milk', methods=['GET'])
def showmilkpage():
    return render_template('milk.html')

# Route to handle the form submission and store data in the database
@app.route('/submit_order', methods=['POST'])
def submit_order():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        customer_id = request.form['customer_id']
        address = request.form['address']
        milk_type = request.form['milk_type']
        liters = request.form['liters']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO orders (name, phone, customer_id, address, milk_type, liters) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, phone, customer_id, address, milk_type, liters))
        mysql.connection.commit()
        cur.close()
         # After inserting the order into the database, generate the bill
        total_price = calculate_total_price(milk_type, liters)  # Implement this function based on your pricing logic

        # Render the bill template with order details
        return render_template('bill.html', name=name, phone=phone, customer_id=customer_id,
                               address=address, milk_type=milk_type, liters=liters, total_price=total_price)

# Function to calculate total price based on milk type and liters
def calculate_total_price(milk_type, liters):
    # Implement pricing logic here
    # Example: If milk type is buffalo milk, price per liter is ₹80
    if milk_type == 'buffalo_milk':
        price_per_liter = 80
    if milk_type == 'cow_milk':
        price_per_liter = 60    
    if milk_type == 'gir_cow_milk':
        price_per_liter = 90      

    # Add more conditions for other milk types if needed

    total_price = float(liters) * price_per_liter
    return total_price
#return redirect('/milk')

# Route to render the shopping page
@app.route('/admin')
def showadminpage():
    return render_template('admin.html')

@app.route('/adminorders')
def showAorderspage():
    return 'DB Milkorders will be displayed here'

# Route to render the aboutus page
@app.route('/aboutus')
def showaboutuspage():
    return render_template('aboutus.html')
# Route to render the contactus page
@app.route('/contactus')
def showcontactpage():
    return '<h1>This is the CONTACT US page of the website.</h1>'

# Route to render the user page "trial"
@app.route('/user', defaults = {"name":"beta_user"})
@app.route('/user/<string:name>')
def showuserpage(name):
    return '<h1>Hello consumer of milk : {}</h1>'.format(name)


@app.route('/subscriber')
def index():
    return render_template('subscriber.html')

@app.route('/submit_subscriber', methods=['POST'])
def submit_subscriber():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        customer_id = request.form['customer_id']
        milk_type = request.form['milk_type']
        liters = request.form['liters']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO subscribers (name, phone, customer_id, milk_type, liters) VALUES (%s, %s, %s, %s, %s)", (name, phone, customer_id, milk_type, liters))
        mysql.connection.commit()
        cur.close()
        return '<h1>Subscriber {} added successfully in system</h1>'.format(name)

@app.route('/dashboard')
def dashboard():
    return 'Dashboard Page'


if __name__=="__main__":
  app.run(debug=True)