"""
ConfigDB with "sqlalchemy" --> danay meneses november 2020
DB: classicmodels
Tables: offices

"""

from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Table, MetaData, select, insert, update, delete
from models import offices, employees


app = Flask(__name__)

engine = create_engine('mysql+pymysql://root:@localhost/pruebadanay')

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
    stm = offices.insert().values(officeCode=officeCode, city=city, phone=phone, addressLine1=addressLine1, addressLine2=addressLine2, state=state, country=country, postalCode=postalCode, territory=territory)
    result = connection.execute(stm)
    return jsonify("Inserted data")


@app.route('/offices/<string:officeCode>', methods=['GET'])
def getoffices(officeCode):
    found = officeCode
    stm = offices.select().where(offices.columns.officeCode == found)
    result = connection.execute(stm)
    c = result.rowcount
    if c == 0:
        return jsonify("Office no exist")
    else:
        for row in result:
            d = dict(row)
            return jsonify(d)


@app.route('/offices/<string:officeCode>', methods=['PATCH'])
def putoffices(officeCode):
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
    stm = offices.update().values(officeCode=officeCode, city=city, phone=phone, addressLine1=addressLine1, addressLine2=addressLine2, state=state, country=country, postalCode=postalCode, territory=territory)
    up_stm = stm.where(offices.columns.officeCode == found)
    result = connection.execute(up_stm)
    return jsonify("Updated data")

@app.route('/offices/<string:officeCode>', methods=['DELETE'])
def deloffices(officeCode):
    found = officeCode
    stm = offices.delete().where(offices.columns.officeCode == found)
    result = connection.execute(stm)
    return jsonify("Deleted rows")

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
    stm = employees.insert().values(employeeNumber=employeeNumber, lastName=lastName, firstName=firstName, extension=extension, email=email, officeCode=officeCode, reportsTo=reportsTo, jobTitle=jobTitle)
    result = connection.execute(stm)
    return jsonify("Inserted data")


@app.route('/employees/<int:employeeNumber>', methods=['GET'])
def getemployee(employeeNumber):
    found = employeeNumber
    stm = employees.select().where(employees.columns.employeeNumber == found)
    result = connection.execute(stm)
    c = result.rowcount
    if c == 0:
        return jsonify("Employee no exist")
    else:
        for row in result:
            d = dict(row)
            return jsonify(d)


@app.route('/employees/<int:employeeNumber>', methods=['PATCH'])
def putemployee(employeeNumber):
    found = employeeNumber
    employeeNumber = request.json['employeeNumber']
    lastName = request.json['lastName']
    firstName = request.json['firstName']
    extension = request.json['extension']
    email = request.json['email']
    officeCode = request.json['officeCode']
    reportsTo = request.json['reportsTo']
    jobTitle = request.json['jobTitle']
    stm = employees.update().values(employeeNumber=employeeNumber, lastName=lastName, firstName=firstName, extension=extension, email=email, officeCode=officeCode, reportsTo=reportsTo, jobTitle=jobTitle)
    up_stm = stm.where(employees.columns.employeeNumber == found)
    result = connection.execute(up_stm)
    return jsonify("Updated data")

@app.route('/employees/<int:employeeNumber>', methods=['DELETE'])
def delemployee(employeeNumber):
    found = employeeNumber
    stm = employees.delete().where(employees.columns.employeeNumber == found)
    result = connection.execute(stm)
    return jsonify("Deleted rows")

if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)
