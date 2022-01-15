from flask import *
import pymysql as pm

con=None
cur=None

app = Flask(__name__)
def connectToDB():
    global con, cur
    con=pm.connect(host="localhost",user="root",password="",database="temple")
    cur=con.cursor()
def disconnectDB():
    cur.close()
    con.close()
def getAllVisitortData():
    connectToDB()
    sq="SELECT * FROM visitor"
    cur.execute(sq)
    data=cur.fetchall()
    disconnectDB()
    return data
def insertToVisitorTable(name,contact,address,mail,date=None):   
    try:
        connectToDB()
        insq="INSERT INTO visitor(name,contact,address,mail,date) VALUES (%s, %s, %s, %s, %s);"
        cur.execute(insq, (name,contact,address,mail,date))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False
def getOneVisitor(id):
    connectToDB()
    siq="SELECT * FROM visitor WHERE id=%s;"
    cur.execute(siq, (id, ))
    data=cur.fetchone()
    disconnectDB()
    return data
 
def updateVisitorToTable(name,contact,address,mail,id,date=None):
    try:
        connectToDB()
        upsq="UPDATE visitor SET name=%s, contact=%s, address=%s, mail=%s, date=%s WHERE id=%s;"
        cur.execute(upsq, (name,contact,address,mail,date,id))
        con.commit()
        disconnectDB()
        return True
    except Exception as e:
        print(e)
        disconnectDB()
        return False
def deletevisitorFromTable(id):
    try:
        connectToDB()
        dsq="DELETE FROM visitor WHERE id=%s;"
        cur.execute(dsq, (id, ))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False
@app.route("/")
@app.route("/hello_world")
def hello_world():
    data= getAllVisitortData()
    return render_template("home.html",data=data)
@app.route("/add/", methods= ['GET', 'POST'])
def addvisitor():
    if request.method == 'POST':
        data=request.form
        if insertToVisitorTable(data['txtName'], data['txtMobile'], data['txtAddress'], data['txtEmail'], data['txtDate']):
           message= "Record inserted succefully"
        else:
          message="Insert Properlly"
        return render_template("frm.html",message=message)
    return render_template("frm.html")
@app.route("/edit/", methods=['GET','POST'])
def updateVisitor():
    id=request.args.get('id', type=int,default=1)
    data= getOneVisitor(id)
    if request.method == 'POST':
        fdata=request.form
        if updateVisitorToTable(fdata['txtName'], fdata['txtMobile'], fdata['txtAddress'] , fdata['txtEmail'], id , fdata['txtDate']):
           message= "Record update succefully"
        else:
          message="Update Properlly"
        return render_template("update.html",message=message)
    return render_template("update.html", data=data)
@app.route("/delete/")
def deleteVisitor():
    id =request.args.get('id', type=int,default=1)
    deletevisitorFromTable(id)
    return redirect(url_for("hello_world"))
if __name__=="__main__":
    app.run()







