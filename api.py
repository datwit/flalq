"""
ConfigDB with "sqlalchemy" --> danay meneses november 2020
DB: classicmodels
Tables: offices

"""

from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Table, MetaData, select, insert, update, delete, and_
from models import offices, employees, customers, payments, orders, orderdetails, productlines, products
from sqlalchemy.exc import IntegrityError
from datetime import datetime
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
        return jsonify("Deleted row")
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
        return jsonify("Deleted row")
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
        return jsonify("Deleted row")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

...
@app.route('/productlines/', methods=['GET'])
def allproductlines():
    table = Table('productlines', metadata, autoload=True, autoload_with=engine)
    stm = select([table])
    result = connection.execute(stm)
    rows = result.fetchall()
    if len(rows) == 0:
        return jsonify("empty table")
    else:
        return str(rows)

@app.route('/productlines/', methods=['POST'])
def postproductlines():
    productLine = request.json['productLine']
    textDescription = request.json['textDescription']
    htmlDescription = request.json['htmlDescription']
    image = request.json['image']
    try:
        stm = productlines.insert().values(
            productLine=productLine,
            textDescription=textDescription,
            htmlDescription=htmlDescription,
            image=image
            )
        result = connection.execute(stm)
        return jsonify("Inserted data")
    except IntegrityError as e:
        return jsonify({"error": str(e)})

@app.route('/productlines/<string:productLine>', methods=['GET'])
def getproductlines(productLine):
    found = productLine
    stm = productlines.select().where(productlines.c.productLine == found)
    result = connection.execute(stm)
    c = result.rowcount
    if c == 0:
        return jsonify("Product Line no exist")
    else:
        for row in result:
            d = dict(row)
            return jsonify(d)

@app.route('/productlines/<string:productLine>', methods=['PATCH'])
def patchproductlines(productLine):
    found = productLine
    textDescription = request.json['textDescription']
    htmlDescription = request.json['htmlDescription']
    image = request.json['image']
    transaction = connection.begin()
    try:
        stm = productlines.update().values(
            textDescription=textDescription,
            htmlDescription=htmlDescription,
            image=image
            )
        up_stm = stm.where(productlines.c.productLine == found)
        result = connection.execute(up_stm)
        transaction.commit()
        return jsonify("Updated data")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

@app.route('/productlines/<string:productLine>', methods=['DELETE'])
def delproductlines(productLine):
    found = productLine
    try:
        stm = productlines.delete().where(productlines.c.productLine == found)
        result = connection.execute(stm)
        return jsonify("Deleted row")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

...
@app.route('/products/', methods=['GET'])
def allproducts():
    table = Table('products', metadata, autoload=True, autoload_with=engine)
    stm = select([table])
    result = connection.execute(stm)
    rows = result.fetchall()
    if len(rows) == 0:
        return jsonify("empty table")
    else:
        return str(rows)

@app.route('/products/', methods=['POST'])
def postproducts():
    productCode = request.json['productCode']
    productName = request.json['productName']
    productLine = request.json['productLine']
    productScale = request.json['productScale']
    productVendor = request.json['productVendor']
    productDescription = request.json['productDescription']
    quantityInStock = request.json['quantityInStock']
    buyPrice = request.json['buyPrice']
    MSRP = request.json['MSRP']
    try:
        stm = products.insert().values(
            productCode=productCode,
            productName=productName,
            productLine=productLine,
            productScale=productScale,
            productVendor=productVendor,
            productDescription=productDescription,
            quantityInStock=quantityInStock,
            buyPrice=buyPrice,
            MSRP=MSRP
            )
        result = connection.execute(stm)
        return jsonify("Inserted data")
    except IntegrityError as e:
        return jsonify({"error": str(e)})

@app.route('/products/<string:productCode>', methods=['GET'])
def getproducts(productCode):
    found = productCode
    stm = products.select().where(products.c.productCode == found)
    result = connection.execute(stm)
    c = result.rowcount
    if c == 0:
        return jsonify("Product no exist")
    else:
        for row in result:
            d = dict(row)
            return jsonify(d)

@app.route('/products/<string:productCode>', methods=['PATCH'])
def patchproducts(productCode):
    found = productCode
    productName = request.json['productName']
    productLine = request.json['productLine']
    productScale = request.json['productScale']
    productVendor = request.json['productVendor']
    productDescription = request.json['productDescription']
    quantityInStock = request.json['quantityInStock']
    buyPrice = request.json['buyPrice']
    MSRP = request.json['MSRP']
    transaction = connection.begin()
    try:
        stm = products.update().values(
            productName=productName,
            productLine=productLine,
            productScale=productScale,
            productVendor=productVendor,
            productDescription=productDescription,
            quantityInStock=quantityInStock,
            buyPrice=buyPrice,
            MSRP=MSRP
            )
        up_stm = stm.where(products.c.productCode == found)
        result = connection.execute(up_stm)
        transaction.commit()
        return jsonify("Updated data")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

@app.route('/products/<string:productCode>', methods=['DELETE'])
def delproducts(productCode):
    found = productCode
    try:
        stm = products.delete().where(products.c.productCode == found)
        result = connection.execute(stm)
        return jsonify("Deleted row")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

...
@app.route('/payments/', methods=['GET'])
def allpayments():
    table = Table('payments', metadata, autoload=True, autoload_with=engine)
    stm = select([table])
    result = connection.execute(stm)
    rows = result.fetchall()
    if len(rows) == 0:
        return jsonify("empty table")
    else:
        return str(rows)

@app.route('/payments/', methods=['POST'])
def postpayments():
    customerNumber = request.json['customerNumber']
    checkNumber = request.json['checkNumber']
    paymentDate = request.json['paymentDate']
    amount = request.json['amount']
    try:
        stm = payments.insert().values(
            customerNumber=customerNumber,
            checkNumber=checkNumber,
            paymentDate=paymentDate,
            amount=amount
            )
        result = connection.execute(stm)
        return jsonify("Inserted data")
    except IntegrityError as e:
        return jsonify({"error": str(e)})

@app.route('/payments/<int:customerNumber>', methods=['GET'])
def getpayments(customerNumber):
    found = customerNumber
    stm = payments.select().where(payments.c.customerNumber == found)
    result = connection.execute(stm)
    c = result.rowcount
    if c == 0:
        return jsonify("Payments no exist")
    else:
        for row in result:
            d = dict(row)
            return jsonify(d)

@app.route('/payments/<int:customerNumber>', methods=['PATCH'])
def patchpayments(customerNumber):
    found = customerNumber
    checkNumber = request.json['checkNumber']
    paymentDate = request.json['paymentDate']
    amount = request.json['amount']
    transaction = connection.begin()
    try:
        stm = payments.update().values(
            paymentDate=paymentDate,
            amount=amount
            )
        up_stm = stm.where(and_(payments.c.customerNumber == found, checkNumber == checkNumber))
        result = connection.execute(up_stm)
        transaction.commit()
        return jsonify("Updated data")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

@app.route('/payments/<int:customerNumber>', methods=['DELETE'])
def delpayments(customerNumber):
    found = customerNumber
    checkNumber = request.json['checkNumber']
    try:
        stm = payments.delete().where(and_(payments.c.customerNumber == found, checkNumber == checkNumber))
        result = connection.execute(stm)
        return jsonify("Deleted row")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

...
@app.route('/orders/', methods=['GET'])
def allorders():
    table = Table('orders', metadata, autoload=True, autoload_with=engine)
    stm = select([table])
    result = connection.execute(stm)
    rows = result.fetchall()
    if len(rows) == 0:
        return jsonify("empty table")
    else:
        return str(rows)

@app.route('/orders/', methods=['POST'])
def postorders():
    orderDate = datetime.now()
    requiredDate = request.json['requiredDate']
    shippedDate = request.json['shippedDate']
    status = request.json['status']
    comments = request.json['comments']
    customerNumber = request.json['customerNumber']
    try:
        stm = orders.insert().values(
            orderDate=orderDate,
            requiredDate=requiredDate,
            shippedDate=shippedDate,
            status=status,
            comments=comments,
            customerNumber=customerNumber
            )
        result = connection.execute(stm)
        return jsonify("Inserted data")
    except IntegrityError as e:
        return jsonify({"error": str(e)})

@app.route('/orders/<int:orderNumber>', methods=['GET'])
def getorders(orderNumber):
    found = orderNumber
    stm = orders.select().where(orders.c.orderNumber == found)
    result = connection.execute(stm)
    c = result.rowcount
    if c == 0:
        return jsonify("Orders no exist")
    else:
        for row in result:
            d = dict(row)
            return jsonify(d)

@app.route('/orders/<int:orderNumber>', methods=['PATCH'])
def patchorders(orderNumber):
    found = orderNumber
    requiredDate = request.json['requiredDate']
    shippedDate = request.json['shippedDate']
    status = request.json['status']
    comments = request.json['comments']
    transaction = connection.begin()
    try:
        stm = orders.update().values(
            requiredDate=requiredDate,
            shippedDate=shippedDate,
            status=status,
            comments=comments,
            )
        up_stm = stm.where(orders.c.orderNumber == found)
        result = connection.execute(up_stm)
        transaction.commit()
        return jsonify("Updated data")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

@app.route('/orders/<int:orderNumber>', methods=['DELETE'])
def delorders(orderNumber):
    found = orderNumber
    try:
        stm = orders.delete().where(orders.c.orderNumber == found)
        result = connection.execute(stm)
        return jsonify("Deleted row")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

...
@app.route('/orderdetails/', methods=['GET'])
def allorderdetails():
    table = Table('orderdetails', metadata, autoload=True, autoload_with=engine)
    stm = select([table])
    result = connection.execute(stm)
    rows = result.fetchall()
    if len(rows) == 0:
        return jsonify("empty table")
    else:
        return str(rows)

@app.route('/orderdetails/', methods=['POST'])
def postorderdetails():
    orderNumber = request.json['orderNumber']
    productCode = request.json['productCode']
    quantityOrdered = request.json['quantityOrdered']
    priceEach = request.json['priceEach']
    orderLineNumber = request.json['orderLineNumber']
    try:
        stm = orderdetails.insert().values(
            orderNumber=orderNumber,
            productCode=productCode,
            quantityOrdered=quantityOrdered,
            priceEach=priceEach,
            orderLineNumber=orderLineNumber
            )
        result = connection.execute(stm)
        return jsonify("Inserted data")
    except IntegrityError as e:
        return jsonify({"error": str(e)})

@app.route('/orderdetails/<int:orderNumber>', methods=['GET'])
def getorderdetails(orderNumber):
    found = orderNumber
    stm = orderdetails.select().where(orderdetails.c.orderNumber == found)
    result = connection.execute(stm)
    c = result.rowcount
    if c == 0:
        return jsonify("Orderdetails no exist")
    else:
        for row in result:
            d = dict(row)
            return jsonify(d)

@app.route('/orderdetails/<int:orderNumber>', methods=['PATCH'])
def patchorderdetails(orderNumber):
    found = orderNumber
    productCode = request.json['productCode']
    quantityOrdered = request.json['quantityOrdered']
    priceEach = request.json['priceEach']
    orderLineNumber = request.json['orderLineNumber']
    transaction = connection.begin()
    try:
        stm = orderdetails.update().values(
            quantityOrdered=quantityOrdered,
            priceEach=priceEach,
            orderLineNumber=orderLineNumber
            )
        up_stm = stm.where(and_(orderdetails.c.orderNumber == found, orderdetails.c.productCode == productCode))
        result = connection.execute(up_stm)
        transaction.commit()
        return jsonify("Updated data")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})

@app.route('/orderdetails/<int:orderNumber>', methods=['DELETE'])
def delorderdetails(orderNumber):
    found = orderNumber
    productCode = request.json['productCode']
    try:
        stm = orderdetails.delete().where(and_(orderdetails.c.orderNumber == found, orderdetails.c.productCode == productCode))
        result = connection.execute(stm)
        return jsonify("Deleted row")
    except IntegrityError as e:
        transaction.rollback()
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)
