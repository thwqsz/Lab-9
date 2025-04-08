from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    link = db.Column(db.String(300))

    def __repr__(self):
        return f'{self.title} - {self.link}'


@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    link = request.form['link']
    project = Project(title=title, link=link)
    db.session.add(project)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear():
    db.session.query(Project).delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
