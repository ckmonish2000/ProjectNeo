from flask import Flask,render_template,url_for,request,redirect
from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String

app=Flask(__name__)

engine=create_engine("sqlite:///models.db",echo=True)
meta=MetaData()

models=Table(
"models",meta,
Column("id",Integer,primary_key=True),
Column("modelName",String),
Column("username",String),
Column("repo",String),
Column("path",String),
Column("modelExtens",String)
)

meta.create_all(engine)

@app.route("/")
def index():
	return render_template("test.html")

@app.route("/upload/",methods=["GET","POST"])
def upload():
	conn=engine.connect()
	if request.method=="POST":
		print(request.form)
		ins=models.insert().values(modelName=request.form["modelname"],username=request.form["gitUserName"],
		repo=request.form["repo"],path=request.form["path"],modelExtens=request.form["exten"])
		conn.execute(ins)

		return redirect(url_for("index"))
	return render_template("upload.html")



@app.route("/models")
def model():
	conn=engine.connect()
	sel=models.select()
	res=conn.execute(sel)
	
	return render_template("view.html",data=res)

@app.route("/webvr/<int:id>")
def page(id):
	conn=engine.connect()
	sel=models.select().where(models.c.id==id)
	res=conn.execute(sel)
	for i in res:
		print(i)
		x=i

	username=x[2]
	repo=x[3]
	path=x[4]
	cdn=f"https://cdn.jsdelivr.net/gh/{username}/{repo}{path}"
	return render_template(f'index.html',s=cdn)


#
# username="ckmonish2000"
# repo="assets"
# path="/scene.gltf"


if __name__=="__main__":
    app.run(debug=True)
