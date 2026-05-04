from extensions import db   # ✅ changed

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    start_date = db.Column(db.String(50))
    description = db.Column(db.Text)
    skills = db.Column(db.Text)
    future_opportunities = db.Column(db.Text)
    max_applicants = db.Column(db.Integer)