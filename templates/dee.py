from flask import Flask, jsonify, request, make_response,render_template,request
from datetime import datetime
import mysql.connector
import json
from mysql.connector import Error
#from flask_cors import CORS, cross_origin



app=Flask(__name__)
 


    
try:
    con=mysql.connector.connect(host="35.232.30.27",user="root",password="password",database="task3")
    con.autocommit=True
    cur = con.cursor(dictionary=True)
    print('Connection Successful')
except Error as e:
    print("Error while connecting to MySQL", e)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/uipost",methods=["GET","POST"])
def post_emp():
    if request.method=="POST":
        name=request.form["name"]
        description=request.form["desig"]
        cur.execute(f"INSERT INTO task3db(id, name, description) VALUES('{id}','{name}','{description}')")

        return render_template("index.html")

    else:
        return render_template("insert.html")

@app.route("/emplist/update",methods=["POST","GET"])
def up_emp():
    if request.method=="POST":
        id=request.form["up"]
        name = request.form["upname"]
        description = request.form["updesig"]
        cur.execute(f"UPDATE task3db set name='{name}',description='{description}' where id={id}")
        return render_template("index.html")
    else:
        return render_template("update.html")

@app.route("/emplist", methods = ["GET"])
def get_emps(self):
    cur.execute("SELECT * FROM task3db")
    result=cur.fetchall()
    if len(result)>0:
        return jsonify(result)
    else:
        return {"message" :"No Data Found"}

@app.route("/emplist/delete",methods=["GET","POST"])
def del_emp():
    if request.method=="POST":
        id=request.form["del"]
        cur.execute(f"DELETE FROM task3db WHERE id={id}")
        return render_template("index.html")

    else:
        return render_template("delete.html")

if __name__=="__main__":
    app.run(debug=True)

    