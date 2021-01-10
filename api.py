#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime
from api.models import Office, Employee, Customer, Payment, Order, Orderdetail, Productline, Product
from api.models import OfficeSchema, EmployeeSchema, CustomerSchema, PaymentSchema, OrderSchema, OrderdetailSchema, ProductlineSchema, ProductSchema
from api.utils import responses as resp


# Create the application instance
app = Flask(__name__)

# Create engine declarative, configure mysql connection
engine = create_engine('mysql+pymysql://root:@localhost/test', echo=True)

# Establish the mysql connection
connection = engine.connect()

# Create session declarative
Session = sessionmaker(bind=engine)
# Instantiate session
session = Session()


# Create a URL route in our application for "/offices/" to read a collection
@app.route('/offices/', methods=['GET'])
def alloffices():
    rows = session.query(Office).order_by(Office.state).all()           # Using order_by to see how work this
    object_schema = OfficeSchema(many=True)
    result = object_schema.dump(rows)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200        # I did many way for this resp. *.bmp

# Create a URL route in our application for "/offices/" to create a new row
@app.route('/offices/', methods=['POST'])
def postoffice():
    try:
        data = request.get_json()
        object_schema = OfficeSchema()
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400   # 422 ó 400 ... ???

# Create a URL route in our application for "/offices/" to read a particular row in the collection
@app.route('/offices/<string:officeCode>', methods=['GET'])
def getoffice(officeCode):
    found = officeCode
    row = session.query(Office).get(found)
    object_schema = OfficeSchema()
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404

# Create a URL route in our application for "/offices/" to update all details of an existing row
@app.route('/offices/<string:officeCode>', methods=['PUT'])
def putoffice(officeCode):
    found = officeCode
    data = request.get_json()
    object_schema = OfficeSchema()
    result = object_schema.dump(data)
    try:
        session.query(Office).filter(Office.officeCode==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400

# Create a URL route in our application for "/offices/" to update some details of an existing row
@app.route('/offices/<string:officeCode>', methods=['PATCH'])
def patchoffice(officeCode):
    found = officeCode
    data = request.get_json()
    row = session.query(Office).get(found)
    try:
        if data.get('phone'):
            row.phone = data['phone']
        if data.get('postalCode'):
            row.postalCode = data['postalCode']
        if data.get('addressLine1'):
            row.addressLine1 = data['addressLine1']
        if data.get('addressLine2'):
            row.addressLine2 = data['addressLine2']
        session.add(row)
        session.commit()
        object_schema = OfficeSchema()
        result = object_schema.dump(row)
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row Fields": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400

# Create a URL route in our application for "/offices/" to delete an existing row
@app.route('/offices/<string:officeCode>', methods=['DELETE'])
def deloffice(officeCode):
    found = officeCode
    try:
        row = session.query(Office).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400       #or 204??


...

@app.route('/employees/', methods=['GET'])
def allemployees():
    rows = session.query(Employee).all()
    object_schema = EmployeeSchema(many=True)
    result = object_schema.dump(rows)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@app.route('/employees/', methods=['POST'])
def postemployee():
    try:
        data = request.get_json()
        object_schema = EmployeeSchema()
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@app.route('/employees/<int:employeeNumber>', methods=['GET'])
def getemployee(employeeNumber):
    found = employeeNumber
    row = session.query(Employee).get(found)
    object_schema = EmployeeSchema()
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@app.route('/employees/<int:employeeNumber>', methods=['PUT'])
def putemployee(employeeNumber):
    found = employeeNumber
    data = request.get_json()
    object_schema = EmployeeSchema()
    result = object_schema.dump(data)
    try:
        session.query(Employee).filter(Employee.employeeNumber==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400












@app.route('/employees/<int:employeeNumber>', methods=['DELETE'])
def delemployee(employeeNumber):
    found = employeeNumber
    try:
        row = session.query(Employee).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


...

@app.route('/customers/', methods=['GET'])
def allcustomers():
    rows = session.query(Customer).all()
    object_schema = CustomerSchema(many=True)
    result = object_schema.dump(rows)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@app.route('/customers/', methods=['POST'])
def postcustomer():
    try:
        data = request.get_json()
        object_schema = CustomerSchema()
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@app.route('/customers/<int:customerNumber>', methods=['GET'])
def getcustomer(customerNumber):
    found = customerNumber
    row = session.query(Customer).get(found)
    object_schema = CustomerSchema()
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200        # "......!!!"
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@app.route('/customers/<int:customerNumber>', methods=['PUT'])
def putcustomer(customerNumber):
    found = customerNumber
    data = request.get_json()
    object_schema = CustomerSchema()
    result = object_schema.dump(data)
    try:
        session.query(Customer).filter(Customer.customerNumber==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400














@app.route('/customers/<int:customerNumber>', methods=['DELETE'])
def delcustomer(customerNumber):
    found = customerNumber
    try:
        row = session.query(Customer).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


...

@app.route('/productlines/', methods=['GET'])
def allproductlines():
    rows = session.query(Productline).all()
    object_schema = ProductlineSchema(many=True)
    result = object_schema.dump(rows)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@app.route('/productlines/', methods=['POST'])
def postproductline():
    try:
        data = request.get_json()
        object_schema = ProductlineSchema()
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@app.route('/productlines/<string:productLine>', methods=['GET'])
def getproductlines(productLine):
    found = productLine
    row = session.query(Productline).get(found)
    object_schema = ProductlineSchema()
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@app.route('/productlines/<string:productLine>', methods=['PUT'])
def putproductlines(productLine):
    found = productLine
    data = request.get_json()
    object_schema = ProductlineSchema()
    result = object_schema.dump(data)
    try:
        session.query(Productline).filter(Productline.productLine==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400












@app.route('/productlines/<string:productLine>', methods=['DELETE'])
def delproductlines(productLine):
    found = productLine
    try:
        row = session.query(Productline).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


...

@app.route('/products/', methods=['GET'])
def allproducts():
    rows = session.query(Product).all()
    object_schema = ProductSchema(many=True)
    result = object_schema.dump(rows)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@app.route('/products/', methods=['POST'])
def postproduct():
    try:
        data = request.get_json()
        object_schema = ProductSchema()
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@app.route('/products/<string:productCode>', methods=['GET'])
def getproducts(productCode):
    found = productCode
    row = session.query(Product).get(found)
    object_schema = ProductSchema()
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@app.route('/products/<string:productCode>', methods=['PUT'])
def putproducts(productCode):
    found = productCode
    data = request.get_json()
    object_schema = ProductSchema()
    result = object_schema.dump(data)
    try:
        session.query(Product).filter(Product.productCode==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400










@app.route('/products/<string:productCode>', methods=['DELETE'])
def delproducts(productCode):
    found = productCode
    try:
        row = session.query(Product).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


...

@app.route('/payments/', methods=['GET'])
def allpayments():
    rows = session.query(Payment).all()
    object_schema = PaymentSchema(many=True)
    result = object_schema.dump(rows)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@app.route('/payments/', methods=['POST'])
def postpayment():
    try:
        data = request.get_json()
        object_schema = PaymentSchema()
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@app.route('/payments/<string:checkNumber>', methods=['GET'])
def getpayments(checkNumber):
    found = checkNumber
    row = session.query(Payment).get(found)
    object_schema = PaymentSchema()
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@app.route('/payments/<string:checkNumber>', methods=['PUT'])
def putpayments(checkNumber):
    found = checkNumber
    data = request.get_json()
    object_schema = PaymentSchema()
    result = object_schema.dump(data)
    try:
        session.query(Payment).filter(Payment.checkNumber==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400










@app.route('/payments/<string:checkNumber>', methods=['DELETE'])
def delpayments(checkNumber):
    found = checkNumber
    try:
        row = session.query(Payment).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


...

@app.route('/orders/', methods=['GET'])
def allorders():
    rows = session.query(Order).all()
    object_schema = OrderSchema(many=True)
    result = object_schema.dump(rows)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@app.route('/orders/', methods=['POST'])
def postorder():
    try:
        data = request.get_json()           # review datetime
        object_schema = OrderSchema()
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@app.route('/orders/<int:orderNumber>', methods=['GET'])
def getorders(orderNumber):
    found = orderNumber
    row = session.query(Order).get(found)
    object_schema = OrderSchema()
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@app.route('/orders/<int:orderNumber>', methods=['PUT'])
def putorders(orderNumber):
    found = orderNumber
    data = request.get_json()
    object_schema = OrderSchema()
    result = object_schema.dump(data)
    try:
        session.query(Order).filter(Order.orderNumber==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400









@app.route('/orders/<int:orderNumber>', methods=['DELETE'])
def delorders(orderNumber):
    found = orderNumber
    try:
        row = session.query(Order).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


...

@app.route('/orderdetails/', methods=['GET'])
def allorderdetails():
    rows = session.query(Orderdetail).all()
    object_schema = OrderdetailSchema(many=True)
    result = object_schema.dump(rows)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


@app.route('/orderdetails/', methods=['POST'])
def postorderdetail():
    try:
        data = request.get_json()           # review datetime
        object_schema = OrderdetailSchema()
        row = object_schema.load(data)
        session.add(row)
        session.commit()
        result = object_schema.dump(data)
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


@app.route('/orderdetails/<int:orderNumber>', methods=['GET'])
def getorderdetails(orderNumber):
    found = orderNumber
    row = session.query(Orderdetail).get(found)
    object_schema = OrderdetailSchema()
    result = object_schema.dump(row)
    if result:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200
    else:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404


@app.route('/orderdetails/<int:orderNumber>', methods=['PUT'])
def putorderdetails(orderNumber):
    found = orderNumber
    data = request.get_json()
    object_schema = OrderdetailSchema()
    result = object_schema.dump(data)
    try:
        session.query(Orderdetail).filter(Orderdetail.orderNumber==found).update(result)
        session.commit()
        return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
    except IntegrityError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400









@app.route('/orderdetails/<int:orderNumber>', methods=['DELETE'])
def delorderdetails(orderNumber):
    found = orderNumber
    try:
        row = session.query(Orderdetail).get(found)
        session.delete(row)
        session.commit()
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    except SQLAlchemyError as error:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)
