from flask import Blueprint, request, session
from models import Opportunity
from extensions import db

opp_bp = Blueprint('opp', __name__)

def get_admin():
    return session.get('admin_id')

@opp_bp.route('/opportunities')
def get_all():
    admin_id = get_admin()
    data = Opportunity.query.filter_by(admin_id=admin_id).all()

    return [{
        "id": o.id,
        "name": o.name,
        "category": o.category,
        "duration": o.duration,
        "start_date": o.start_date,
        "description": o.description
    } for o in data]

@opp_bp.route('/opportunity', methods=['POST'])
def create():
    admin_id = get_admin()
    data = request.json

    opp = Opportunity(
        admin_id=admin_id,
        name=data['name'],
        category=data['category'],
        duration=data['duration'],
        start_date=data['start_date'],
        description=data['description'],
        skills=data['skills'],
        future_opportunities=data['future_opportunities'],
        max_applicants=data.get('max_applicants')
    )

    db.session.add(opp)
    db.session.commit()

    return {"message": "Created"}

@opp_bp.route('/opportunity/<int:id>', methods=['PUT'])
def update(id):
    admin_id = get_admin()
    opp = Opportunity.query.get(id)

    if opp.admin_id != admin_id:
        return {"error": "Unauthorized"}, 403

    data = request.json

    for key in data:
        setattr(opp, key, data[key])

    db.session.commit()

    return {"message": "Updated"}

@opp_bp.route('/opportunity/<int:id>', methods=['DELETE'])
def delete(id):
    admin_id = get_admin()
    opp = Opportunity.query.get(id)

    if opp.admin_id != admin_id:
        return {"error": "Unauthorized"}, 403

    db.session.delete(opp)
    db.session.commit()

    return {"message": "Deleted"}