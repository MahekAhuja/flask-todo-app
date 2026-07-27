from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

# Create database
with app.app_context():
    db.create_all()

# Home Route (Show all Todos)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        new_todo = Todo(title=title, desc=desc)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

# Delete Route
@app.route('/delete/<int:sno>')
def delete(sno):
    task = Todo.query.filter_by(sno=sno).first()
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('home'))

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)