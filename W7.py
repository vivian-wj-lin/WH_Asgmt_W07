from unicodedata import name
from flask import Flask, render_template, request, redirect, session
import mysql.connector
import mysql.connector.cursor
app = Flask(
    __name__,
    static_folder="templates",
    static_url_path="/"
)

app.secret_key = "secret"

IS_LOGIN = "isLogin..."

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysqlpwd2022",
    database="mysql"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS week7")
mydb.commit()
mycursor.close()
mydb.close()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysqlpwd2022",
    database="week7"
)
mycursor = mydb.cursor()
mycursor.execute(
    '''
    CREATE Table IF NOT EXISTS member
    (
        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        name varchar(20) not null,
        username varchar(20) not null UNIQUE,
        password char(20) not null
    );
    '''
)
mydb.commit()


@app.route("/")
def index():
    return render_template("W6.html")


@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]

    # 檢查帳號
    mycursor = mydb.cursor()
    select_stmt = "SELECT * FROM member WHERE username = %(username)s"
    mycursor.execute(select_stmt, {"username": username})
    myresult = mycursor.fetchall()

    if not myresult:
        mycursor = mydb.cursor()
        sql = "INSERT INTO member (name,username,password) VALUES (%s, %s, %s)"
        val = [(name, username, password)]
        mycursor.executemany(sql, val)
        mydb.commit()
        return redirect("/")

    else:
        return redirect("/error?message=帳號已經被註冊")


@app.route("/member")
def index_member():
    if session.get(IS_LOGIN, None):
        return render_template("member.html", Hello=session["name"])
    return redirect("/")


@app.route("/api/member")
def search_name():
    if session.get(IS_LOGIN, None):
        username = request.args.get("username")
        mycursor = mydb.cursor()
        select_stmt = "SELECT id, name, username FROM member WHERE username = %(username)s"
        mycursor.execute(select_stmt, {"username": username})
        select_stmt = mycursor.fetchone()
        return {
            "data": {"id": select_stmt[0], "name": select_stmt[1], "username": select_stmt[2]}
        }
    else:
        return {"data": None}


@ app.route("/api/member", methods=["PATCH"])
def name():
    if session.get(IS_LOGIN, None):
        new_name = request.get_json()["name"]
        # print(new_name)  # new name
        # print(session["name"])  # old name
        mycursor = mydb.cursor()
        select_stmt = "UPDATE member SET name = %(new_name)s WHERE name = %(name)s"
        mycursor.execute(
            select_stmt, {"name": session["name"], "new_name": new_name})
        mydb.commit()
        mycursor.close()

        session["name"] = new_name

        return new_name


@ app.route("/signout")
def signout():
    session[IS_LOGIN] = False  # 設定登出為 False
    return redirect("/")


@ app.route("/error")
def index_error():
    message = request.args.get("message")
    return render_template("signInFailure.html", reason=message)


@ app.route("/signin", methods=["POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    if (username == "" or password == ""):
        return redirect("/error?message=請輸入帳號、密碼")
    mycursor = mydb.cursor()
    select_stmt = "SELECT name FROM member WHERE username = %s AND password = %s"
    mycursor.execute(select_stmt, (username, password))
    myresult = mycursor.fetchall()[0][0]  # name

    if myresult:
        session[IS_LOGIN] = True
        session["name"] = myresult
        return redirect("/member")

    if not myresult:
        return redirect("/error?message=帳號、或密碼輸入錯誤")


app.run(debug=True, port=3000)

# python W7.py
