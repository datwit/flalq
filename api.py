#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import IntegrityError
from datetime import datetime
from models import Office, Employee, Customer, Payment, Order, Orderdetail, Productline, Product
from models import OfficeSchema, EmployeeSchema, CustomerSchema, PaymentSchema, OrderSchema, OrderdetailSchema, ProductlineSchema, ProductSchema
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
        return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": row}), resp.SUCCESS_201
    except Exception as e:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400   # 422 ó 400 ... ???

# Create a URL route in our application for "/offices/" to read a particular row in the collection
@app.route('/offices/<string:officeCode>', methods=['GET'])
def getoffice(officeCode):
    found = officeCode
    row = session.query(Office).get(found)
    object_schema = OfficeSchema()
    result = object_schema.dump(row)
    if len(result) == 0:
        return resp.response_with(resp.SERVER_ERROR_404), resp.SERVER_ERROR_404
    else:
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200

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
    except Exception as e:
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
    except Exception as e:
        session.rollback()
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400

# Create a URL route in our application for "/offices/" to delete an existing row
@app.route('/offices/<string:officeCode>', methods=['DELETE'])
def deloffice(officeCode):
    found = officeCode
    row = session.query(Office).get(found)
    session.delete(row)
    session.commit()
    return jsonify("Deleted Row")


...
# @app.route('/employees/', methods=['GET'])
# def allemployees():
#     rows = session.query(Employee).all()
#     if len(rows) == 0:
#         return jsonify("Empty Table")
#     else:
#         employee_schema = EmployeeSchema(many=True)
#         result = employee_schema.dump(rows)
#         return jsonify(result)

#     stm = employees.select()
#     result = connection.execute(stm)
#     rows = result.fetchall()
#     if len(rows) == 0:
#         return jsonify("empty table")
#     else:
#         l = []
#         for row in rows:
#             d = {"employeeNumber": row[0], "lastName": row[1], "firstName":row[2], "extension": row[3], "email": row[4], "officeCode": row[5], "reportsTo": row[6], "jobTitle": row[7]}
#             l.append(d)
#         return jsonify(l)

# @app.route('/employees/', methods=['POST'])
# def postemployees():
#     employeeNumber = request.json['employeeNumber']
#     lastName = request.json['lastName']
#     firstName = request.json['firstName']
#     extension = request.json['extension']
#     email = request.json['email']
#     officeCode = request.json['officeCode']
#     reportsTo = request.json['reportsTo']
#     jobTitle = request.json['jobTitle']
#     try:
#         stm = employees.insert().values(
#             employeeNumber=employeeNumber,
#             lastName=lastName,
#             firstName=firstName,
#             extension=extension,
#             email=email,
#             officeCode=officeCode,
#             reportsTo=reportsTo,
#             jobTitle=jobTitle
#             )
#         result = connection.execute(stm)
#         return jsonify("Inserted data")
#     except IntegrityError as e:
#         return jsonify({"error": str(e)})

# @app.route('/employees/<int:employeeNumber>', methods=['GET'])
# def getemployee(employeeNumber):
#     found = employeeNumber
#     stm = employees.select().where(employees.c.employeeNumber == found)
#     result = connection.execute(stm)
#     c = result.rowcount
#     if c == 0:
#         return jsonify("Employee no exist")
#     else:
#         row = result.first()
#         return jsonify(dict(row))

# @app.route('/employees/<int:employeeNumber>', methods=['PUT'])
# def putemployee(employeeNumber):
#     found = employeeNumber
#     lastName = request.json['lastName']
#     firstName = request.json['firstName']
#     extension = request.json['extension']
#     email = request.json['email']
#     officeCode = request.json['officeCode']
#     reportsTo = request.json['reportsTo']
#     jobTitle = request.json['jobTitle']
#     transaction = connection.begin()
#     try:
#         stm = employees.update().values(
#             lastName=lastName,
#             firstName=firstName,
#             extension=extension,
#             email=email,
#             officeCode=officeCode,
#             reportsTo=reportsTo,
#             jobTitle=jobTitle
#             )
#         up_stm = stm.where(employees.c.employeeNumber == found)
#         result = connection.execute(up_stm)
#         transaction.commit()
#         return jsonify("Updated data")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# @app.route('/employees/<int:employeeNumber>', methods=['DELETE'])
# def delemployee(employeeNumber):
#     found = employeeNumber
#     try:
#         stm = employees.delete().where(employees.c.employeeNumber == found)
#         result = connection.execute(stm)
#         return jsonify("Deleted row")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# ...
# @app.route('/customers/', methods=['GET'])
# def allcustomers():
#     stm = customers.select()
#     result = connection.execute(stm)
#     rows = result.fetchall()
#     if len(rows) == 0:
#         return jsonify("empty table")
#     else:
#         l = []
#         for row in rows:
#             d = {"customerNumber": row[0], "customerName": row[1], "contactLastName":row[2], "contactFirstName": row[3], "phone": row[4], "addressLine1": row[5], "addressLine2": row[6], "city": row[7], "state": row[8], "postalCode": row[9], "country": row[10], "salesRepEmployeeNumber": row[11], "creditLimit": float(row[12])}
#             l.append(d)
#         return jsonify(l)

# @app.route('/customers/', methods=['POST'])
# def postcustomers():
#     customerNumber = request.json['customerNumber']
#     customerName = request.json['customerName']
#     contactLastName = request.json['contactLastName']
#     contactFirstName = request.json['contactFirstName']
#     phone = request.json['phone']
#     addressLine1 = request.json['addressLine1']
#     addressLine2 = request.json['addressLine2']
#     city = request.json['city']
#     state = request.json['state']
#     postalCode = request.json['postalCode']
#     country = request.json['country']
#     salesRepEmployeeNumber = request.json['salesRepEmployeeNumber']
#     creditLimit = request.json['creditLimit']
#     try:
#         stm = customers.insert().values(
#             customerNumber=customerNumber,
#             customerName=customerName,
#             contactLastName=contactLastName,
#             contactFirstName=contactFirstName,
#             phone=phone,
#             addressLine1=addressLine1,
#             addressLine2=addressLine2,
#             city=city,
#             state=state,
#             postalCode=postalCode,
#             country=country,
#             salesRepEmployeeNumber=salesRepEmployeeNumber,
#             creditLimit=creditLimit
#             )
#         result = connection.execute(stm)
#         return jsonify("Inserted data")
#     except IntegrityError as e:
#         return jsonify({"error": str(e)})

# @app.route('/customers/<int:customerNumber>', methods=['GET'])
# def getcustomer(customerNumber):
#     found = customerNumber
#     stm = customers.select().where(customers.c.customerNumber == found)
#     result = connection.execute(stm)
#     c = result.rowcount
#     if c == 0:
#         return jsonify("Customer no exist")
#     else:
#         l = []
#         row = result.first()
#         d = {"customerNumber": row[0], "customerName": row[1], "contactLastName":row[2], "contactFirstName": row[3], "phone": row[4], "addressLine1": row[5], "addressLine2": row[6], "city": row[7], "state": row[8], "postalCode": row[9], "country": row[10], "salesRepEmployeeNumber": row[11], "creditLimit": float(row[12])}
#         return jsonify(d)               # ¡¡¡ ... I made it! At last! ... !!!

# @app.route('/customers/<int:customerNumber>', methods=['PUT'])
# def putcustomer(customerNumber):
#     found = customerNumber
#     customerName = request.json['customerName']
#     contactLastName = request.json['contactLastName']
#     contactFirstName = request.json['contactFirstName']
#     phone = request.json['phone']
#     addressLine1 = request.json['addressLine1']
#     addressLine2 = request.json['addressLine2']
#     city = request.json['city']
#     state = request.json['state']
#     postalCode = request.json['postalCode']
#     country = request.json['country']
#     salesRepEmployeeNumber = request.json['salesRepEmployeeNumber']
#     creditLimit = request.json['creditLimit']
#     transaction = connection.begin()
#     try:
#         stm = customers.update().values(
#             customerName=customerName,
#             contactLastName=contactLastName,
#             contactFirstName=contactFirstName,
#             phone=phone,
#             addressLine1=addressLine1,
#             addressLine2=addressLine2,
#             city=city,
#             state=state,
#             postalCode=postalCode,
#             country=country,
#             salesRepEmployeeNumber=salesRepEmployeeNumber,
#             creditLimit=creditLimit
#             )
#         up_stm = stm.where(customers.c.customerNumber == found)
#         result = connection.execute(up_stm)
#         transaction.commit()
#         return jsonify("Updated data")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# @app.route('/customers/<int:customerNumber>', methods=['DELETE'])
# def delcustomer(customerNumber):
#     found = customerNumber
#     try:
#         stm = customers.delete().where(customers.c.customerNumber == found)
#         result = connection.execute(stm)
#         return jsonify("Deleted row")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# ...
# @app.route('/productlines/', methods=['GET'])
# def allproductlines():
#     stm = productlines.select()
#     result = connection.execute(stm)
#     rows = result.fetchall()
#     if len(rows) == 0:
#         return jsonify("empty table")
#     else:
#         l = []
#         for row in rows:
#             d = {"productLine": row[0], "textDescription": row[1], "htmlDescription":row[2], "image": row[3]}
#             l.append(d)
#         return jsonify(l)

# @app.route('/productlines/', methods=['POST'])
# def postproductlines():
#     productLine = request.json['productLine']
#     textDescription = request.json['textDescription']
#     htmlDescription = request.json['htmlDescription']
#     image = request.json['image']
#     try:
#         stm = productlines.insert().values(
#             productLine=productLine,
#             textDescription=textDescription,
#             htmlDescription=htmlDescription,
#             image=image
#             )
#         result = connection.execute(stm)
#         return jsonify("Inserted data")
#     except IntegrityError as e:
#         return jsonify({"error": str(e)})

# @app.route('/productlines/<string:productLine>', methods=['GET'])
# def getproductlines(productLine):
#     found = productLine
#     stm = productlines.select().where(productlines.c.productLine == found)
#     result = connection.execute(stm)
#     c = result.rowcount
#     if c == 0:
#         return jsonify("Product Line no exist")
#     else:
#         row = result.first()
#         return jsonify(dict(row))

# @app.route('/productlines/<string:productLine>', methods=['PUT'])
# def putproductlines(productLine):
#     found = productLine
#     textDescription = request.json['textDescription']
#     htmlDescription = request.json['htmlDescription']
#     image = request.json['image']
#     transaction = connection.begin()
#     try:
#         stm = productlines.update().values(
#             textDescription=textDescription,
#             htmlDescription=htmlDescription,
#             image=image
#             )
#         up_stm = stm.where(productlines.c.productLine == found)
#         result = connection.execute(up_stm)
#         transaction.commit()
#         return jsonify("Updated data")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# @app.route('/productlines/<string:productLine>', methods=['DELETE'])
# def delproductlines(productLine):
#     found = productLine
#     try:
#         stm = productlines.delete().where(productlines.c.productLine == found)
#         result = connection.execute(stm)
#         return jsonify("Deleted row")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# ...
# @app.route('/products/', methods=['GET'])
# def allproducts():
#     stm = products.select()
#     result = connection.execute(stm)
#     rows = result.fetchall()
#     if len(rows) == 0:
#         return jsonify("empty table")
#     else:
#         l = []
#         for row in rows:
#             d = {"productCode": row[0], "productName": row[1], "productLine":row[2], "productScale": row[3], "productVendor": row[4], "productDescription": row[5], "quantityInStock": row[6], "buyPrice": float(row[7]), "MSRP": float(row[8])}
#             l.append(d)
#         return jsonify(l)

# @app.route('/products/', methods=['POST'])
# def postproducts():
#     productCode = request.json['productCode']
#     productName = request.json['productName']
#     productLine = request.json['productLine']
#     productScale = request.json['productScale']
#     productVendor = request.json['productVendor']
#     productDescription = request.json['productDescription']
#     quantityInStock = request.json['quantityInStock']
#     buyPrice = request.json['buyPrice']
#     MSRP = request.json['MSRP']
#     try:
#         stm = products.insert().values(
#             productCode=productCode,
#             productName=productName,
#             productLine=productLine,
#             productScale=productScale,
#             productVendor=productVendor,
#             productDescription=productDescription,
#             quantityInStock=quantityInStock,
#             buyPrice=buyPrice,
#             MSRP=MSRP
#             )
#         result = connection.execute(stm)
#         return jsonify("Inserted data")
#     except IntegrityError as e:
#         return jsonify({"error": str(e)})

# @app.route('/products/<string:productCode>', methods=['GET'])
# def getproducts(productCode):
#     found = productCode
#     stm = products.select().where(products.c.productCode == found)
#     result = connection.execute(stm)
#     c = result.rowcount
#     if c == 0:
#         return jsonify("Product no exist")
#     else:
#         l = []
#         row = result.first()
#         d = {"productCode": row[0], "productName": row[1], "productLine":row[2], "productScale": row[3], "productVendor": row[4], "productDescription": row[5], "quantityInStock": row[6], "buyPrice": float(row[7]), "MSRP": float(row[8])}
#         return jsonify(d) 

# @app.route('/products/<string:productCode>', methods=['PUT'])
# def putproducts(productCode):
#     found = productCode
#     productName = request.json['productName']
#     productLine = request.json['productLine']
#     productScale = request.json['productScale']
#     productVendor = request.json['productVendor']
#     productDescription = request.json['productDescription']
#     quantityInStock = request.json['quantityInStock']
#     buyPrice = request.json['buyPrice']
#     MSRP = request.json['MSRP']
#     transaction = connection.begin()
#     try:
#         stm = products.update().values(
#             productName=productName,
#             productLine=productLine,
#             productScale=productScale,
#             productVendor=productVendor,
#             productDescription=productDescription,
#             quantityInStock=quantityInStock,
#             buyPrice=buyPrice,
#             MSRP=MSRP
#             )
#         up_stm = stm.where(products.c.productCode == found)
#         result = connection.execute(up_stm)
#         transaction.commit()
#         return jsonify("Updated data")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# @app.route('/products/<string:productCode>', methods=['DELETE'])
# def delproducts(productCode):
#     found = productCode
#     try:
#         stm = products.delete().where(products.c.productCode == found)
#         result = connection.execute(stm)
#         return jsonify("Deleted row")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# ...
# @app.route('/payments/', methods=['GET'])
# def allpayments():
#     stm = payments.select()
#     result = connection.execute(stm)
#     rows = result.fetchall()
#     if len(rows) == 0:
#         return jsonify("empty table")
#     else:
#         l = []
#         for row in rows:
#             d = {"customerNumber": row[0], "checkNumber": row[1], "paymentDate":row[2], "amount": float(row[3])}
#             l.append(d)
#         return jsonify(l)

# @app.route('/payments/', methods=['POST'])
# def postpayments():
#     customerNumber = request.json['customerNumber']
#     checkNumber = request.json['checkNumber']
#     paymentDate = request.json['paymentDate']
#     amount = request.json['amount']
#     try:
#         stm = payments.insert().values(
#             customerNumber=customerNumber,
#             checkNumber=checkNumber,
#             paymentDate=paymentDate,
#             amount=amount
#             )
#         result = connection.execute(stm)
#         return jsonify("Inserted data")
#     except IntegrityError as e:
#         return jsonify({"error": str(e)})

# @app.route('/payments/<string:checkNumber>', methods=['GET'])
# def getpayments(checkNumber):
#     found = checkNumber
#     stm = payments.select().where(payments.c.checkNumber == found)
#     result = connection.execute(stm)
#     c = result.rowcount
#     if c == 0:
#         return jsonify("Payments no exist")
#     else:
#         l = []
#         row = result.first()
#         d = {"customerNumber": row[0], "checkNumber": row[1], "paymentDate":row[2], "amount": float(row[3])}
#         return jsonify(d)


# @app.route('/payments/<string:checkNumber>', methods=['PUT'])
# def putpayments(checkNumber):
#     found = checkNumber
#     paymentDate = request.json['paymentDate']
#     amount = request.json['amount']
#     transaction = connection.begin()
#     try:
#         stm = payments.update().values(
#             paymentDate=paymentDate,
#             amount=amount
#             )
#         up_stm = stm.where(payments.c.checkNumber == found)
#         result = connection.execute(up_stm)
#         transaction.commit()
#         return jsonify("Updated data")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# @app.route('/payments/<string:checkNumber>', methods=['DELETE'])
# def delpayments(checkNumber):
#     found = checkNumber
#     try:
#         stm = payments.delete().where(payments.c.checkNumber == found)
#         result = connection.execute(stm)
#         return jsonify("Deleted row")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# ...
# @app.route('/orders/', methods=['GET'])
# def allorders():
#     stm = orders.select()
#     result = connection.execute(stm)
#     rows = result.fetchall()
#     if len(rows) == 0:
#         return jsonify("empty table")
#     else:
#         l = []
#         for row in rows:
#             d = {"orderNumber": row[0], "orderDate": row[1], "requiredDate":row[2], "shippedDate": row[3], "status": row[4], "comments": row[5], "customerNumber": row[6]}
#             l.append(d)
#         return jsonify(l)

# @app.route('/orders/', methods=['POST'])
# def postorders():
#     orderDate = datetime.now                           # using the callable 'datetime.now' instead of the function call itself, 'datetime.now()'
#     requiredDate = request.json['requiredDate']
#     shippedDate = request.json['shippedDate']
#     status = request.json['status']
#     comments = request.json['comments']
#     customerNumber = request.json['customerNumber']
#     try:
#         stm = orders.insert().values(
#             orderDate=orderDate,
#             requiredDate=requiredDate,
#             shippedDate=shippedDate,
#             status=status,
#             comments=comments,
#             customerNumber=customerNumber
#             )
#         result = connection.execute(stm)
#         return jsonify("Inserted data")
#     except IntegrityError as e:
#         return jsonify({"error": str(e)})

# @app.route('/orders/<int:orderNumber>', methods=['GET'])
# def getorders(orderNumber):
#     found = orderNumber
#     stm = orders.select().where(orders.c.orderNumber == found)
#     result = connection.execute(stm)
#     c = result.rowcount
#     if c == 0:
#         return jsonify("Orders no exist")
#     else:
#         row = result.first()
#         return jsonify(dict(row))

# @app.route('/orders/<int:orderNumber>', methods=['PUT'])
# def putorders(orderNumber):
#     found = orderNumber
#     requiredDate = request.json['requiredDate']
#     shippedDate = request.json['shippedDate']
#     status = request.json['status']
#     comments = request.json['comments']
#     transaction = connection.begin()
#     try:
#         stm = orders.update().values(
#             requiredDate=requiredDate,
#             shippedDate=shippedDate,
#             status=status,
#             comments=comments,
#             )
#         up_stm = stm.where(orders.c.orderNumber == found)
#         result = connection.execute(up_stm)
#         transaction.commit()
#         return jsonify("Updated data")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# @app.route('/orders/<int:orderNumber>', methods=['DELETE'])
# def delorders(orderNumber):
#     found = orderNumber
#     try:
#         stm = orders.delete().where(orders.c.orderNumber == found)
#         result = connection.execute(stm)
#         return jsonify("Deleted row")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# ...
# @app.route('/orderdetails/', methods=['GET'])
# def allorderdetails():
#     stm = orderdetails.select()
#     result = connection.execute(stm)
#     rows = result.fetchall()
#     if len(rows) == 0:
#         return jsonify("empty table")
#     else:
#         l = []
#         for row in rows:
#             d = {"orderNumber": row[0], "productCode": row[1], "quantityOrdered":row[2], "priceEach": float(row[3]), "orderLineNumber": row[4]}
#             l.append(d)
#         return jsonify(l)

# @app.route('/orderdetails/', methods=['POST'])
# def postorderdetails():
#     orderNumber = request.json['orderNumber']
#     productCode = request.json['productCode']
#     quantityOrdered = request.json['quantityOrdered']
#     priceEach = request.json['priceEach']
#     orderLineNumber = request.json['orderLineNumber']
#     try:
#         stm = orderdetails.insert().values(
#             orderNumber=orderNumber,
#             productCode=productCode,
#             quantityOrdered=quantityOrdered,
#             priceEach=priceEach,
#             orderLineNumber=orderLineNumber
#             )
#         result = connection.execute(stm)
#         return jsonify("Inserted data")
#     except IntegrityError as e:
#         return jsonify({"error": str(e)})

# @app.route('/orderdetails/<int:orderNumber>', methods=['GET'])
# def getorderdetails(orderNumber):
#     found = orderNumber
#     stm = orderdetails.select().where(orderdetails.c.orderNumber == found)
#     result = connection.execute(stm)
#     c = result.rowcount
#     if c == 0:
#         return jsonify("Orderdetails no exist")
#     else:
#         l = []
#         rows = result.fetchall()
#         for row in rows:
#             d = {"orderNumber": row[0], "productCode": row[1], "quantityOrdered":row[2], "priceEach": float(row[3]), "orderLineNumber": row[4]}
#             l.append(d)
#         return jsonify(l)

# @app.route('/orderdetails/<int:orderNumber>', methods=['PUT'])
# def putorderdetails(orderNumber):
#     found = orderNumber
#     productCode = request.json['productCode']
#     quantityOrdered = request.json['quantityOrdered']
#     priceEach = request.json['priceEach']
#     orderLineNumber = request.json['orderLineNumber']
#     transaction = connection.begin()
#     try:
#         stm = orderdetails.update().values(
#             quantityOrdered=quantityOrdered,
#             priceEach=priceEach,
#             orderLineNumber=orderLineNumber
#             )
#         up_stm = stm.where(and_(orderdetails.c.orderNumber == found, orderdetails.c.productCode == productCode))
#         result = connection.execute(up_stm)
#         transaction.commit()
#         return jsonify("Updated data")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})

# @app.route('/orderdetails/<int:orderNumber>', methods=['DELETE'])
# def delorderdetails(orderNumber):
#     found = orderNumber
#     productCode = request.json['productCode']
#     try:
#         stm = orderdetails.delete().where(and_(orderdetails.c.orderNumber == found, orderdetails.c.productCode == productCode))
#         result = connection.execute(stm)
#         return jsonify("Deleted row")
#     except IntegrityError as e:
#         transaction.rollback()
#         return jsonify({"error": str(e)})
# session.close()

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)
