from flask import Flask, jsonify, request, json
import sqlite3
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

app = Flask(__name__)

# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'nodejs_login1'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JWT_SECRET_KEY'] = 'secret'
#
# mysql = MySQL(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)
#Uncomment when have db
@app.route('/api/auth/register/', methods=['POST'])
def register():
    id = ''
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    email = request.get_json()['username']
    password = request.get_json()['password']
    dob = request.get_json()['dob']
    cur.execute("SELECT * FROM user where email = '" + str(email) + "'")
    rv = cur.fetchone()
    if not rv:
        cur.execute("INSERT INTO user (email, password, dob, avatar) VALUES ('" +
            str(email) + "', '" +
            str(password) + "', '" +
            str(dob) + "', '" +
            "" + "')")
        conn.commit()
        cur.execute("SELECT * FROM user where email = '" + str(email) + "'")
        rv = cur.fetchone()
        id = rv[0]
	else:
        id = rv[0]
        email = rv[1]
        password = rv[2]
        dob = rv[3]
    # result = {
	# 	'email' : email,
	# 	'password' : password,
	# 	'dob' : dob,
	# 	'avatar' : avatar
	#   }
    # conn.close()
    access_token = create_access_token(identity = {'email': email}).decode('ascii')
    result = {
        'id': id
        'email' : email,
        'password' : password,
        'dob' : dob,
    }
    return jsonify({'result' : result}), 201
	
@app.route('/api/auth/login/', methods=['POST'])
def login():
    conn = sqlite3.connect('database.db')
    status =""
    cur = conn.cursor()
    email = request.get_json()['username']
    password = request.get_json()['password']
    result = ""
    cur.execute("SELECT * FROM user where email = '" + str(email) + "'")
    rv = cur.fetchone()
    print rv
    if rv[2] == password:
        print "hello"
        access_token = create_access_token(identity = {'email': rv[1]})
        id = rv[0]
        email = rv[1]
        password = rv[2]
        dob = rv[3]
        result = {
            'id': id
            'email' : email,
            'password' : password,
            'dob' : dob,
        }
        jsonify({'result' : result})
        status = 201
    else:
        result = jsonify({"error":"Invalid username and password"})
        status = 403
    conn.close()

    return jsonify({'result' : result}), status

@app.route('/api/auth/user/', methods=['POST'])
def user_auth():
    print request.get_json()
    return null

@app.route('/api/blogs/', methods=['POST'])
def addBlogs():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    userid = request.get_json()['userid']
    title = request.get_json()['title']
    content = request.get_json()['userid']
    conn = sqlite3.connect('database.db')
    cur.execute("INSERT INTO blog (userId, title, content, createdDate) VALUES ('" +
                str(userid) + "', '" +
                str(title) + "', '" +
                str(content) + "', '" +
                str(datetime.now()) + "')")
    conn.commit()
    result = {
            'userid': id
            'title' : title,
            'content' : content,
        }
    conn.close()
    return {},201

@app.route('/api/blogs/', methods=['GET'])
def get_blogs_user_by_id():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    userid = request.get_json()['userid']
    cur.execute("SELECT * FROM blog where userId = '" + str(userid) + "'")
    rv = cur.fetchall()
    blogs[]
    for row in rv:
        blog = {
            'title' : row[2],
            'content' : row[3],
            'createdDate': row[4]
        }
        blogs.append(blog)
    result = {'data': blog}
    
    conn.close()
    return result,201

@app.route('/api/users/', methods=['GET'])
def get_all_users():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    userid = request.get_json()['userid']
    cur.execute("SELECT * FROM user ")
    rv = cur.fetchall()
    users[]
    for row in rv:
        cur.execute("SELECT * FROM relationship where (userId1 = '" + str(userid) + "' and userId2 = '" + str(row[0]) + "') or (userId1 = '" + str(row[0]) + "' and userId2 = '" + str(userid) + "')")
        instance = cur.fetchone()
        is_friend = "FRIEND" if instance else "GUEST"
        user = {
            'id': row[0]
            'email' : row[1],
            'dob' : row[3],
            'relation': is_friend
        }
        users.append(blog)
    result = {'data': users}
    conn.close()
    return result,201

@app.route('/api/users/${userId}/', methods=['GET'])
def get_user_by_id():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    userid = request.get_json()['userid']
    cur.execute("SELECT * FROM user where id = '" + str(userid) + "'")
    rv = cur.fetchone()
    result = {
            'id': rv[0]
            'email' : rv[1],
            'dob' : rv[3],
        }
    conn.close()
    return jsonify({'result' : result}),201

if __name__ == '__main__':
    app.run(debug=True)