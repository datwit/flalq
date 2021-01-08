#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  ForeignKey, Column, String, Integer, SmallInteger, Float, Date, DateTime, Binary, CheckConstraint
from sqlalchemy.sql import func
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields



# Create engine declarative, configure mysql connection
engine = create_engine('mysql+pymysql://root:@localhost/test', echo=True)  # , encoding='latin1')

# Create base declarative
Base = declarative_base()

# Create session declarative
Session = sessionmaker(bind=engine)
# Instantiate session
session = Session()

# Office class
class Office(Base):
    __tablename__ = "offices"

    officeCode = Column(String(10), primary_key=True)
    city = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False, unique=True)         # phone --> validate unique
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50))
    state = Column(String(50))
    country = Column(String(50), nullable=False)
    postalCode = Column(String(15), nullable=False)
    territory = Column(String(10), nullable=False)

    def __init__(self, officeCode, city, phone, addressLine1, addressLine2, state, country, postalCode, territory):
        self.officeCode = officeCode
        self.city = city
        self.phone = phone
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.state = state
        self.country = country
        self.postalCode = postalCode
        self.territory = territory

    def create(self):
        session.add(self)
        session.commit()
        return self

# Office schema
class OfficeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                               # "???"
        model = Office                                          # "???"
        sqla_session = session                                  # "???"

    officeCode = fields.String(required=True)       # dump_only=True --> only reading, to Autocompleted primary key, autocreated Date, file path
    city = fields.String(required=True)
    phone = fields.String(required=True)
    addressLine1 = fields.String(required=True)
    addressLine2 = fields.String(required=True)        # Marshmallow Error: Fields may not be null
    state = fields.String()
    country = fields.String(required=True)
    postalCode = fields.String(required=True)
    territory = fields.String(required=True)



# Employees class
class Employee(Base):
    __tablename__ = "employees"

    employeeNumber = Column(Integer, primary_key=True)          # Integer and primary_key is auto-incremented automatically in table structure
    lastName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    extension = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False, unique=True)                                           # email --> I make it unique
    officeCode = Column(String(10), ForeignKey('offices.officeCode'), nullable=False,)
    reportsTo = Column(Integer, ForeignKey('employees.employeeNumber'))
    jobTitle = Column(String(50), nullable=False)

    def __init__(self, employeeNumber, lastName, firstName, extension, email, jobTitle, officeCode=None, reportsTo=None):
        self.employeeNumber = employeeNumber
        self.lastName = lastName
        self.firstName = firstName
        self.extension = extension
        self.email = email
        self.officeCode = officeCode
        self.reportsTo = reportsTo
        self.jobTitle = jobTitle

    def create(self):
        session.add(self)
        session.commit()
        return self

# Employee schema
class EmployeeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                                                                       # "???"
        model = Employee                                                                                # "???"
        sqla_session = session                                                                          # "???"

    employeeNumber = fields.Integer(dump_only=True)
    lastName = fields.String(required=True)
    firstName = fields.String(required=True)
    extension = fields.String(required=True)
    email = fields.String(required=True)                                                                # validate email format
    officeCode = fields.Nested(OfficeSchema, many=False, only=['officeCode'], required=True)
    reportsTo = fields.Integer()
    jobTitle = fields.String(required=True)



# Productlines class
class Productline(Base):
    __tablename__ = "productlines"

    productLine = Column(String(50), primary_key=True)
    textDescription = Column(String(4000))
    htmlDescription = Column(String(200))                               # validated html format??
    image = Column(Binary)                                              # validate file extension in the path

    def __init__(self, productLine, textDescription, htmlDescription, image):
        self.productLine = productLine
        self.textDescription = textDescription
        self.htmlDescription = htmlDescription
        self.image = image

    def create(self):
        session.add(self)
        session.commit()
        return self

# Customer schema
class ProductlineSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                                       # "???"
        model = Productline                                             # "???"
        sqla_session = session                                     # "???"

    productLine = fields.String(dump_only=True)
    textDescription = fields.String()
    htmlDescription = fields.String()
    image = fields.String()                                             # path to image



# Products class
class Product(Base):
    __tablename__ = "products"

    productCode = Column(String(15), primary_key=True)
    productName = Column(String(70), nullable=False)
    productLine = Column(String(50), ForeignKey('productlines.productLine'), nullable=False)
    productScale = Column(String(10), nullable=False)
    productVendor = Column(String(50), nullable=False)
    productDescription = Column(String(500), nullable=False)
    quantityInStock = Column(SmallInteger, nullable=False)
    buyPrice = Column(Float(10,2), nullable=False)
    MSRP = Column(Float(10,2), nullable=False)
    CheckConstraint('quantityInStock >= 0', name='quantityInStock_positive')        # I am ensuring that quantityInStock data is always positive

    def __init__(self, productCode, productName, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP, productLine=None):
        self.productCode = productCode
        self.productName = productName
        self.productLine = productLine
        self.productScale = productScale
        self.productVendor = productVendor
        self.productDescription = productDescription
        self.quantityInStock = quantityInStock
        self.buyPrice = buyPrice
        self.MSRP = MSRP

    def create(self):
        session.add(self)
        session.commit()
        return self

# Customer schema
class ProductSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                                       # "???"
        model = Product                                                 # "???"
        sqla_session = session                                          # "???"

    productCode = fields.String(dump_only=True)
    productName = fields.String(required=True)
    productLine = fields.Nested(Productline, many=False, only=['productLine'], required=True)
    productScale = fields.String(required=True)
    productVendor = fields.String(required=True)
    productDescription = fields.String(required=True)
    quantityInStock = fields.Integer(required=True)                     # marchmellow have not SmallInteger fields
    buyPrice = fields.Float(required=True)
    MSRP = fields.Float(required=True)



# Customers class
class Customer(Base):
    __tablename__ = "customers"

    customerNumber = Column(Integer, primary_key=True)
    customerName = Column(String(50), nullable=False)
    contactLastName = Column(String(50), nullable=False)
    contactFirstName = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False, unique=True)         # phone --> I make it unique
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50))
    city = Column(String(50), nullable=False)
    state = Column(String(50))
    postalCode = Column(String(15))
    country = Column(String(50), nullable=False)
    salesRepEmployeeNumber = Column(Integer, ForeignKey('employees.employeeNumber'))
    creditLimit = Column(Float(10,2))                          # Float --> because Decimal or Numeric type is not JSON serializable

    def __init__(self, customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2, city, state, postalCode, country, creditLimit, salesRepEmployeeNumber=None):
        self.customerName = customerNumber
        self.customerName = customerName
        self.contactLastName = contactLastName
        self.contactFirstName = contactFirstName
        self.phone = phone
        self.addressLine1 = addressLine1
        self.addressLine2 = addressLine2
        self.city = city
        self.state = state
        self.postalCode = postalCode
        self.country = country
        self.salesRepEmployeeNumber = salesRepEmployeeNumber
        self.creditLimit = creditLimit

    def create(self):
        session.add(self)
        session.commit()
        return self

# Customer schema
class CustomerSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                                       # "???"
        model = Customer                                                # "???"
        sqla_session = session                                          # "???"

    customerNumber = fields.Integer(dump_only=True)
    customerName = fields.String(required=True)
    contactLastName = fields.String(required=True)
    contactFirstName = fields.String(required=True)
    phone = fields.String(required=True)
    addressLine1 = fields.String(required=True)
    addressLine2 = fields.String()
    city = fields.String(required=True)
    state = fields.String()
    postalCode = fields.String()
    country = fields.String(required=True)
    salesRepEmployeeNumber = fields.Nested(Employee, many=True, only=['employeeNumber'])
    creditLimit = fields.Float()



# Orders class
class Order(Base):
    __tablename__ = "orders"

    orderNumber = Column(Integer, primary_key=True)
    orderDate = Column(DateTime, server_default=func.now(), nullable=False)      # orderDate --> Autocomplete on table in created moment
    requiredDate = Column(Date, nullable=False)
    shippedDate = Column(Date)
    status = Column(String(15), nullable=False)     # Status field --> this should be like schedule with many options by default, in other table
    comments = Column(String(500))
    customerNumber = Column(Integer, ForeignKey('customers.customerNumber'), nullable=False,)

    def __init__(self, orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber=None):
        self.orderNumber = orderNumber
        self.orderDate = orderDate
        self.requiredDate = requiredDate
        self.shippedDate = shippedDate
        self.state = state
        self.comments = comments
        self.customerNumber = customerNumber

    def create(self):
        session.add(self)
        session.commit()
        return self

# Customer schema
class OrderSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                                # "???"
        model = Order                                            # "???"
        sqla_session = session                                   # "???"

    orderNumber = fields.Integer(dump_only=True)
    orderDate = fields.Date(dump_only=True)
    requiredDate = fields.Date(required=True)
    shippedDate = fields.Date()
    status = fields.String(required=True)
    comments = fields.String()
    customerNumber = fields.Nested(Customer, many=False, only=['customerNumber'], required=True)



# Orderdetails class
class Orderdetail(Base):
    __tablename__ = "orderdetails"

    orderNumber = Column(Integer, ForeignKey('orders.orderNumber'), primary_key=True)
    productCode = Column(String(15), ForeignKey('products.productCode'), nullable=False, primary_key=True)
    quantityOrdered = Column(Integer, nullable=False)
    priceEach = Column(Float(10,2), nullable=False)
    orderLineNumber = Column(SmallInteger, nullable=False)

    def __init__(self, quantityInStock, priceEach, orderLineNumber, orderNumber=None, productCode=None):
        self.orderNumber = orderNumber
        self.productCode = productCode
        self.quantityOrdered = quantityInStock
        self.priceEach = priceEach
        self.orderLineNumber = orderLineNumber

    def create(self):
        session.add(self)
        session.commit()
        return self

# Customer schema
class OrderdetailSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                               # "???"
        model = Orderdetail                                     # "???"
        sqla_session = session                                  # "???"

    orderNumber = fields.Nested(Order, many=False, only=['orderNumber'], dump_only=True)
    productCode = fields.Nested(Product, many=False, only=['productCode'], required=True)
    quantityOrdered = fields.Integer(required=True)
    priceEach = fields.Float(required=True)
    orderLineNumber = fields.Integer(required=True)                     # marchmellow have not SmallInteger fields



# Payments class
class Payment(Base):
    __tablename__ = "payments"

    customerNumber = Column(Integer, ForeignKey('customers.customerNumber'), primary_key=True,)
    checkNumber = Column(String(50), nullable=False, primary_key=True)
    paymentDate = Column(Date, nullable=False)
    amount = Column(Float(10,2), nullable=False)

    def __init__(self, checkNumber, paymentDate, amount, customerNumber=None):
        self.customerNumber = customerNumber
        self.checkNumber = checkNumber
        self.paymentDate = paymentDate
        self.amount = amount

    def create(self):
        session.add(self)
        session.commit()
        return self

# Customer schema
class PaymentSchema(ModelSchema):
    class Meta(ModelSchema.Meta):                                       # "???"
        model = Payment                                                 # "???"
        sqla_session = session                                          # "???"

    customerNumber = fields.Nested(Customer, many=False, only=['customerNumber'], dump_only=True)
    checkNumber = fields.String(required=True)
    paymentDate = fields.Date(required=True)
    amount = fields.Float(required=True)


Base.metadata.create_all(engine)