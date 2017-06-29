from flask import Flask, render_template, redirect, request, session, flash
import re
from mysqlconnection import MySQLConnector

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = "mermaidsAreReal"
mysql = MySQLConnector(app, 'email_validation')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    query = "SELECT * FROM users"
    emails = mysql.query_db(query)
    last_email = mysql.query_db("SELECT * FROM users ORDER BY id desc LIMIT 1;")

    if len(last_email) < 1:
        last = ""
    else:
        last = last_email[0]['email']
    return render_template('success.html', entered_emails=emails, email=last)

@app.route('/validate', methods=['POST'])
def validate():
    if len(request.form['email']) < 1 or not EMAIL_REGEX.match(request.form['email']):
        flash("Please enter a valid email!")

    if '_flashes' in session:
        return redirect('/')
    else:
        query = "INSERT INTO users (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
            'email': request.form['email']
        }
        mysql.query_db(query, data)
        return redirect('/success')

@app.route('/delete', methods=['POST'])
def delete():
    query = "DELETE FROM users WHERE id = :id"
    data = {
        'id': request.form['id']
    }
    mysql.query_db(query, data)
    return redirect('/success')

@app.route('/return', methods=['POST'])
def home():
    return redirect('/')

app.run(debug=True)
