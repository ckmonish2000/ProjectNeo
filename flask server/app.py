from flask import Flask,render_template,url_for
app=Flask(__name__)

@app.route("/webvr")
def page():
	username="ckmonish2000"
	repo="assets"
	path="/scene.gltf"
	cdn=f"https://cdn.jsdelivr.net/gh/{username}/{repo}{path}"
	return render_template(f'index.html',s=cdn)


@app.route("/")
def index():
	a={"val":[1,2,3,4],"head":"NUMBERS"}
	return render_template("test.html",data=a)



if __name__=="__main__":
    app.run(debug=True)
