from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.app = app

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/")
def index():
    # from models import Todo
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:todo_id>", methods=["GET", "POST"])
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if request.method == 'GET':
        return render_template("update.html", todo = todo)
    elif request.method == 'POST':
        todo.title = request.form.get("title")
        todo.complete = request.form.get("complete") #not todo.complete
        db.session.commit()
        return redirect(url_for("index"))
    

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)