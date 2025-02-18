# app/routes.py
from flask import Blueprint, request, jsonify, abort
from app import db
from app.models import Employee

bp = Blueprint('employees', __name__)

@bp.route('/employees', methods=['GET'])
def get_employees():
    """Retrieve all employees."""
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees]), 200

@bp.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    """Retrieve a single employee by id."""
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict()), 200

@bp.route('/employees', methods=['POST'])
def create_employee():
    """Create a new employee."""
    data = request.get_json() or {}
    if not all(field in data for field in ['name', 'email', 'position']):
        abort(400, "Missing required fields: name, email, position")
    
    # Check if email already exists
    if Employee.query.filter_by(email=data['email']).first():
        abort(400, "Employee with this email already exists")
    
    employee = Employee(
        name=data['name'],
        email=data['email'],
        position=data['position']
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify(employee.to_dict()), 201

@bp.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    """Update an existing employee."""
    employee = Employee.query.get_or_404(id)
    data = request.get_json() or {}
    
    employee.name = data.get('name', employee.name)
    employee.email = data.get('email', employee.email)
    employee.position = data.get('position', employee.position)
    
    db.session.commit()
    return jsonify(employee.to_dict()), 200

@bp.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    """Delete an employee."""
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted successfully."}), 200
