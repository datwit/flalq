"""
ConfigDB with "sqlalchemy" --> danay meneses november 2020
DB: classicmodels
Tables: offices

"""

from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Table, MetaData, select, insert, update, delete
# from sqlalchemy import Column, Integer, Text, , 

app = Flask(__name__)

engine = create_engine('mysql+pymysql://root:@localhost/pruebadanay')

connection = engine.connect()
metadata = MetaData()


# GET ALL
@app.route('/offices/', methods=['GET'])
def alloffices():
    r = Table('offices', metadata, autoload=True, autoload_with=engine)
    stm = select([r])
    result = connection.execute(stm).fetchall()
    if len(result) == 0:
        return jsonify("empty table")
    else:
        return jsonify("resultado pendiente de extraer")


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
    r = Table('offices', metadata, autoload=True, autoload_with=engine)
    stm = insert(r).values(officeCode=officeCode, city=city, phone=phone, addressLine1=addressLine1, addressLine2=addressLine2, state=state, country=country, postalCode=postalCode, territory=territory)
    result = connection.execute(stm)
    return jsonify("Inserted data")


@app.route('/offices/<string:officeCode>', methods=['GET'])
def getoffices(officeCode):
    found = officeCode
    r = Table('offices', metadata, autoload=True, autoload_with=engine)
    stm = select([r]).where(r.columns.officeCode == found)
    result = connection.execute(stm)
    c = result.rowcount
    if c == 0:
        return jsonify("Office no exist")
    else:
        for row in result:
            d = dict(row)
            return jsonify(d)


@app.route('/offices/<string:officeCode>', methods=['PUT'])
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
    r = Table('offices', metadata, autoload=True, autoload_with=engine)
    stm = update(r).values(officeCode=officeCode, city=city, phone=phone, addressLine1=addressLine1, addressLine2=addressLine2, state=state, country=country, postalCode=postalCode, territory=territory)
    up_stm = stm.where(r.columns.officeCode == found)
    result = connection.execute(up_stm)
    return jsonify("Updated data")

@app.route('/offices/<string:officeCode>', methods=['DELETE'])
def deloffices(officeCode):
    found = officeCode
    r = Table('offices', metadata, autoload=True, autoload_with=engine)
    stm = delete(r).where(r.columns.officeCode == found)
    result = connection.execute(stm)
    return jsonify("Deleted rows")


if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)
