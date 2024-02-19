from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import datetime

class TodoForm(FlaskForm):
    todo = StringField(validators=[DataRequired()])
    submit = SubmitField("Add ToDo")

app = Flask(__name__)

app.app_context().push()

app.config['SECRET_KEY'] = "21ugygxcv54gfugygx45xcve4s"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

db.create_all()

@app.route("/", methods=['GET', 'POST'])
def home():
    form = TodoForm()
    current_year = datetime.datetime.now().year
    all_todos = db.session.query(Todos).all()
    return render_template('index.html', year=current_year, form=form, all_todos=all_todos)

@app.route("/add", methods=['GET', 'POST'])
def add():
    form = TodoForm()
    if form.validate_on_submit():
        new_todo = Todos(todo=form.todo.data)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('home'))

@app.route("/delete/<int:todo_id>", methods=['GET', 'POST'])
def delete(todo_id):
    todo = db.session.query(Todos).get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/update/<int:todo_id>", methods=['GET', 'POST'])
def update(todo_id):
    todo = db.session.query(Todos).get(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)