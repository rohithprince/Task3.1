from flask import Flask, jsonify, request, make_response,render_template,request
from datetime import datetime
import mysql.connector
import json
from mysql.connector import Error
from flask_cors import CORS, cross_origin




app=Flask(__name__)
CORS(app)
cors=CORS(app,resources={
    r"/*":{
        "origins":"*"
    }
})


    
try:
    con=mysql.connector.connect(host="34.170.159.224",user="root",password="password",database="task3")
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
        cur.execute(f"INSERT INTO task3db(name, description) VALUES('{name}','{description}')")

        return render_template("index.html")

    else:
        return render_template("insert.html")

@app.route("/emplist", methods = ["POST"])
def add_emp():
    try:
        id=request.json["id"]
        name=request.json["name"]
        description=request.json["designation"]
        cur.execute(f"INSERT INTO task3db(id, name, description) VALUES('{id}','{name}','{description}')")
        cur.execute("SELECT * FROM task3db")
        result=cur.fetchall()

        return jsonify(result)
    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})

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

@app.route("/emplist/put/<int:id>", methods=["PUT"])
def update_emp(id):

    try:
        name = request.json['name']
        description = request.json['designation']
        cur.execute(f"UPDATE task3db set name='{name}',description='{description}' where id={id}")
    except Exception as e:
        return jsonify({"Error": "Invalid request, please try again."})
    cur.execute("SELECT * FROM task3db")
    result=cur.fetchall()    
    return jsonify(result)
# to get all data 
@app.route("/emplist", methods = ["GET"])
def get_emps():
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

@app.route("/emplist/delete/<int:id>", methods=["DELETE"])
def delete_emp(id):
    cur.execute(f"DELETE FROM task3db WHERE id={id}")
    return jsonify({"Success" : "Emp deleted."})

if __name__=="__main__":
    app.run(debug=True)

    
