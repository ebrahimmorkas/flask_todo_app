from flask import Flask, render_template, request, url_for, redirect
# Flask-MySQLdb ---> package nme to be used with mysql and we had installed it with the help of pip
from flask_mysqldb import MySQL
import os
app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = os.environ.get('USERN')
app.config['MYSQL_PASSWORD'] = os.environ.get('PASS')
app.config['MYSQL_DB'] = "todo_flask"

mysql = MySQL(app)

# This is the home route and it will show all the routes on home page
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    data = cur.fetchall()
    return render_template('index.html', items=data)

# Route for handling the submission of form and inserting the record in the database
@app.route('/handle_form', methods=['POST'])
def insert_item():
    cur = mysql.connection.cursor()
    data = request.form
    title = data['title']
    description = data['description']
    insert_query = "Insert into items (title, description) VALUES (%s, %s)"
    values = (title, description)
    cur.execute(insert_query, values)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('home'))

@app.route('/delete', methods=['GET'])
def delete_item():
    item_id = request.args.get('id')
    cur = mysql.connection.cursor()
    delete_query = "DELETE FROM items WHERE id = %s"
    values = (item_id,)
    cur.execute(delete_query, values)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)