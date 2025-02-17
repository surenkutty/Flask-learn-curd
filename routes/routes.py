from flask import Blueprint, request, jsonify, current_app as app
from models.employee import Employee
from extension import db

routes = Blueprint('routes', __name__)

@routes.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    if not all(key in data for key in ('name', 'email', 'position')):
        return jsonify({'error': 'Missing fields'}), 400
    new_employee = Employee(name=data['name'], email=data['email'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify(new_employee.to_dict()), 201

@routes.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees])

@routes.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict())

@routes.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.json
    employee.name = data['name']
    employee.email = data['email']
    employee.position = data['position']
    db.session.commit()
    return jsonify(employee.to_dict())

@routes.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'})

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404
