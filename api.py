"""
ConfigDB with "sqlalchemy" --> danay meneses november 2020
DB: classicmodels
Tables: offices

"""

from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Table, MetaData, select, insert, update, delete
from models import offices, employees, customers, payments, orders, orderdetails, productlines, products
from sqlalchemy.exc import IntegrityError
import status


app = Flask(__name__)

engine = create_engine('mysql+pymysql://root:@localhost/pruebadanay')  # , encoding='latin1')

connection = engine.connect()
metadata = MetaData()


@app.route('/offices/', methods=['GET'])
def alloffices():
    table = Table('offices', metadata, autoload=True, autoload_with=engine)
    stm = select([table])
    result = connection.execute(stm)
    rows = result.fetchall()
    if len(rows) == 0:
        return jsonify("empty table")
    else:
        return str(rows)

@app.route('/offices/', methods=['POST'])
def postoffices():
    officeCode = request.json['officeCode']
    city = request.json['city']
    phone = request.json['phone']
    addressLine1 = request.json['addressLine1']
    addressLine2 = request.json['addressLine2']
    state = request.json['state']
    country = request.json['country']
    postalCode = request.json['postalCode']
    territory = request.json['territory']
    try:
        stm = offices.insert().values(
            officeCode=officeCode,
            city=city, phone=phone,
            addressLine1=addressLine1,
            addressLine2=addressLine2,
            state=state,
            country=country,
            postalCode=postalCode,
            territory=territory
            )
        result = connection.execute(stm)
        return jsonify("Inserted data")
    except IntegrityError as e:
        return jsonify({"error": str(e)})

@app.route('/offices/<string:officeCode>', methods=['GET'])
def getoffices(officeCode):
    found = officeCode
    stm = offices.select().where(offices.c.officeCode == found)
    result = connection.execute(stm)
    c = result.rowcount
    if c == 0:
        return jsonify("Office no exist")
    else:
        for row in result:
            d = dict(row)
            return jsonify(d)

@app.route('/offices/<string:officeCode>', methods=['PATCH'])
def patchoffices(officeCode):
    found = officeCode
    officeCode = request.json['officeCode']
    city = request.json['city']
    phone = request.json['phone']
    addressLine1 = request.json['addressLine1']
    addressLine2 = request.json['addressLine2']
    state = request.json['state']
    country = request.json['country']
    postalCode = request.json['postalCode']
    territory = request.json['territory']
    transaction = connection.begin()
    try:
        stm = offices.update().values(
            officeCode=officeCode,
            city=city,
            phone=phone,
            addressLine1=addressLine1,
            addressLine2=addressLine2,
            state=state,
            country=country,
            postalCode=postalCode,
            territory=territory
            )
        up_stm = stm.where(offices.c.officeCode == found)
        result = connection.execute(up_stm)
        transaction.commit()
        return jsonify("Updated data")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

@app.route('/offices/<string:officeCode>', methods=['DELETE'])
def deloffices(officeCode):
    found = officeCode
    try:
        stm = offices.delete().where(offices.c.officeCode == found)
        result = connection.execute(stm)
        return jsonify("Deleted rows")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

...
@app.route('/employees/', methods=['GET'])
def allemployees():
    table = Table('employees', metadata, autoload=True, autoload_with=engine)
    stm = select([table])
    result = connection.execute(stm)
    rows = result.fetchall()
    if len(rows) == 0:
        return jsonify("empty table")
    else:
        return str(rows)

@app.route('/employees/', methods=['POST'])
def postemployees():
    employeeNumber = request.json['employeeNumber']
    lastName = request.json['lastName']
    firstName = request.json['firstName']
    extension = request.json['extension']
    email = request.json['email']
    officeCode = request.json['officeCode']
    reportsTo = request.json['reportsTo']
    jobTitle = request.json['jobTitle']
    try:
        stm = employees.insert().values(
            employeeNumber=employeeNumber,
            lastName=lastName,
            firstName=firstName,
            extension=extension,
            email=email,
            officeCode=officeCode,
            reportsTo=reportsTo,
            jobTitle=jobTitle
            )
        result = connection.execute(stm)
        return jsonify("Inserted data")
    except IntegrityError as e:
        return jsonify({"error": str(e)})

@app.route('/employees/<int:employeeNumber>', methods=['GET'])
def getemployee(employeeNumber):
    found = employeeNumber
    stm = employees.select().where(employees.c.employeeNumber == found)
    result = connection.execute(stm)
    c = result.rowcount
    if c == 0:
        return jsonify("Employee no exist")
    else:
        for row in result:
            d = dict(row)
            return jsonify(d)

@app.route('/employees/<int:employeeNumber>', methods=['PATCH'])
def patchemployee(employeeNumber):
    found = employeeNumber
    employeeNumber = request.json['employeeNumber']
    lastName = request.json['lastName']
    firstName = request.json['firstName']
    extension = request.json['extension']
    email = request.json['email']
    officeCode = request.json['officeCode']
    reportsTo = request.json['reportsTo']
    jobTitle = request.json['jobTitle']
    transaction = connection.begin()
    try:
        stm = employees.update().values(
            employeeNumber=employeeNumber,
            lastName=lastName,
            firstName=firstName,
            extension=extension,
            email=email,
            officeCode=officeCode,
            reportsTo=reportsTo,
            jobTitle=jobTitle
            )
        up_stm = stm.where(employees.c.employeeNumber == found)
        result = connection.execute(up_stm)
        transaction.commit()
        return jsonify("Updated data")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

@app.route('/employees/<int:employeeNumber>', methods=['DELETE'])
def delemployee(employeeNumber):
    found = employeeNumber
    try:
        stm = employees.delete().where(employees.c.employeeNumber == found)
        result = connection.execute(stm)
        return jsonify("Deleted rows")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

...
@app.route('/customers/', methods=['GET'])
def allcustomers():
    table = Table('customers', metadata, autoload=True, autoload_with=engine)
    stm = select([table])
    result = connection.execute(stm)
    rows = result.fetchall()
    if len(rows) == 0:
        return jsonify("empty table")
    else:
        return str(rows)

@app.route('/customers/', methods=['POST'])
def postcustomers():
    customerNumber = request.json['customerNumber']
    customerName = request.json['customerName']
    contactLastName = request.json['contactLastName']
    contactFirstName = request.json['contactFirstName']
    phone = request.json['phone']
    addressLine1 = request.json['addressLine1']
    addressLine2 = request.json['addressLine2']
    city = request.json['city']
    state = request.json['state']
    postalCode = request.json['postalCode']
    country = request.json['country']
    salesRepEmployeeNumber = request.json['salesRepEmployeeNumber']
    creditLimit = request.json['creditLimit']
    try:
        stm = customers.insert().values(
            customerNumber=customerNumber,
            customerName=customerName,
            contactLastName=contactLastName,
            contactFirstName=contactFirstName,
            phone=phone,
            addressLine1=addressLine1,
            addressLine2=addressLine2,
            city=city,
            state=state,
            postalCode=postalCode,
            country=country,
            salesRepEmployeeNumber=salesRepEmployeeNumber,
            creditLimit=creditLimit
            )
        result = connection.execute(stm)
        return jsonify("Inserted data")
    except IntegrityError as e:
        return jsonify({"error": str(e)})

@app.route('/customers/<int:customerNumber>', methods=['GET'])
def getcustomer(customerNumber):
    found = customerNumber
    stm = customers.select().where(customers.c.customerNumber == found)
    result = connection.execute(stm)
    c = result.rowcount
    if c == 0:
        return jsonify("Customer no exist")
    else:
        for row in result:
            d = dict(row)
            return jsonify(d)   #error: Object of type Decimal is not JSON serializable

@app.route('/customers/<int:customerNumber>', methods=['PATCH'])
def patchcustomer(customerNumber):
    found = customerNumber
    customerNumber = request.json['customerNumber']
    customerName = request.json['customerName']
    contactLastName = request.json['contactLastName']
    contactFirstName = request.json['contactFirstName']
    phone = request.json['phone']
    addressLine1 = request.json['addressLine1']
    addressLine2 = request.json['addressLine2']
    city = request.json['city']
    state = request.json['state']
    postalCode = request.json['postalCode']
    country = request.json['country']
    salesRepEmployeeNumber = request.json['salesRepEmployeeNumber']
    creditLimit = request.json['creditLimit']
    transaction = connection.begin()
    try:
        stm = customers.update().values(
            customerNumber=customerNumber,
            customerName=customerName,
            contactLastName=contactLastName,
            contactFirstName=contactFirstName,
            phone=phone,
            addressLine1=addressLine1,
            addressLine2=addressLine2,
            city=city,
            state=state,
            postalCode=postalCode,
            country=country,
            salesRepEmployeeNumber=salesRepEmployeeNumber,
            creditLimit=creditLimit
            )
        up_stm = stm.where(customers.c.customerNumber == found)
        result = connection.execute(up_stm)
        transaction.commit()
        return jsonify("Updated data")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

@app.route('/customers/<int:customerNumber>', methods=['DELETE'])
def delcustomer(customerNumber):
    found = customerNumber
    try:
        stm = customers.delete().where(customers.c.customerNumber == found)
        result = connection.execute(stm)
        return jsonify("Deleted rows")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)
