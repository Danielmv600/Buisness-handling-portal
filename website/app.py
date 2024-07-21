from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messages

# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vaishu@2004",
    database="wbtb"
)
mycursor = mydb.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hm', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        sql = "SELECT * FROM webtble WHERE email = %s AND passwrd = %s"
        values = (email, password)
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        if result:
            # User exists, redirect to dashboard
            session['username'] = result[1]  # Store username in session
            return render_template('dashboard.html')
        else:
            # User does not exist, show an error message
            flash("Invalid email or password", 'error')
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/sgn', methods=["GET","POST"])
def sign():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Debug: Print received form data
        print(f"Received: username={username}, email={email}, password={password}")

        # Check if username already exists
        sql_check_user = "SELECT * FROM webtble WHERE username = %s"
        mycursor.execute(sql_check_user, (username,))
        existing_user = mycursor.fetchone()

        if existing_user:
            flash("Username already exists. Please choose a different username.", 'error')
            return redirect(url_for('sign'))

        try:
            # Insert new user into the database
            sql_insert_user = "INSERT INTO webtble (username, email, passwrd) VALUES (%s, %s, %s)"
            mycursor.execute(sql_insert_user, (username, email, password))
            mydb.commit()  # Commit the transaction
            # Debug: Print success message
            print("User added successfully.")
        except mysql.connector.Error as err:
            # Debug: Print error message
            print(f"Error: {err}")
            flash("An error occurred while signing up. Please try again.", 'error')
            return redirect(url_for('sign'))

        flash("Signup successful! Please login with your credentials.", 'success')
        return redirect(url_for('home'))
    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('home'))

@app.route('/abstract')
def abstract():
    return render_template('abstract.html')

@app.route('/logout')
def logout():
    # Handle logout logic here (e.g., clearing session data)
    # Redirect to login page after logout
    session.pop('user_id', None)  # Remove user session
    return redirect(url_for('home'))

@app.route('/stock-details')
def stock_details():
    return render_template('stock-details.html')

@app.route('/next')
def next_pg():
    return render_template('next-page.html')

@app.route('/cosmetics')
def ele_brand():
    return render_template('next-page1.html')

@app.route('/shoes')
def cos_brand():
    return render_template('next-page2.html')

@app.route('/gucci')
def brnd1():
    return render_template('brnd1.html')


if __name__ == '__main__':
    app.run(debug=True)
