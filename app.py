from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://login:pass@localhost/my_db'
db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    finish_date = db.Column(db.Date, nullable=True)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    begin_date = db.Column(db.Date)


@app.route('/')
def index():
    return render_template('new_base.html', tasks=Task.query.order_by(Task.id).all())


@app.route('/add', methods=["POST"])
def add():
    text = request.form.get('task')
    details = request.form.get('details')
    db.session.add(
        Task(text=text, details=details, start_date=date.today())
    )
    print(text + "\n" + details + "\n" + str(date.today()))
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/clear', methods=["POST"])
def clear():
    Task.query.delete()    
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/done/<int:task_id>')
def done(task_id):
    task = Task.query.get(task_id)   
    task.is_done = True
    task.finish_date = date.today()
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/reopen/<int:task_id>')
def reopen(task_id):
    task = Task.query.get(task_id)
    task.is_done = False
    task.finish_date = None
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    
