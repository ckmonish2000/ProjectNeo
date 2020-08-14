from flask import Flask,render_template,url_for,request,redirect
from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String
import graphene
from flask_cors import CORS,cross_origin
from flask_graphql import GraphQLView
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

class Models(graphene.ObjectType):
	id=graphene.Int()
	modelName=graphene.String()
	username=graphene.String()
	repo=graphene.String()
	path=graphene.String()
	modelexe=graphene.String()

class Query(graphene.ObjectType):
	modellist=graphene.List(Models)

	def resolve_modellist(root,info):
		conn=engine.connect()
		sel=models.select()
		res=conn.execute(sel)
		lst=[]
		for i in res:
			print(i)
			lst.append(Models(id=i[0],modelName=i[1],username=i[2],repo=i[3],path=i[4],modelexe=i[5]))
		return lst


schema=graphene.Schema(query=Query)

result=schema.execute('''
{
modellist{
	modelName
}
}
'''
)
print(result.data)


CORS(app, allow_headers=['Content-Type'])

app.add_url_rule('/graphql',
                 view_func=GraphQLView.as_view(
                     'graphql',
                     schema=schema,
                     graphiql=True,
                 ))

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




@app.route("/vr-models")
def vrmodel():
	conn=engine.connect()
	sel=models.select()
	res=conn.execute(sel)

	return render_template("view.html",data=res)


@app.route("/webvr/<int:id>")
def vrpage(id):
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
	print(cdn)
	return render_template(f'index.html',s=cdn)



@app.route("/ar-models")
def armodel():
	conn=engine.connect()
	sel=models.select()
	res=conn.execute(sel)

	return render_template("arview.html",data=res)

@app.route("/webar/<int:id>")
def arpage(id):
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
	print(cdn)
	return render_template(f'ar.html',s=cdn)





#hardcoded values
# username="ckmonish2000"
# repo="assets"
# path="/scene.gltf"

@app.route("/delete/<vue>/<int:id>")
def delete(id,vue):
	conn=engine.connect()
	dele=models.delete().where(models.c.id==id)
	conn.execute(dele)
	if(vue=="vr"):
		return redirect(url_for("vrmodel"))
	else:
		return redirect(url_for("armodel"))





if __name__=="__main__":
    app.run(debug=True)
