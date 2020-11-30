"""
ConfigDB with "sqlalchemy" --> danay meneses november 2020
DB: classicmodels
Tables: all

"""

from sqlalchemy import create_engine
from sqlalchemy import MetaData, ForeignKey, Table, Column, String, Integer, SmallInteger, Numeric, Date, Binary, CheckConstraint

engine = create_engine('mysql+pymysql://root:@localhost/pruebadanay')            #  , encoding='latin1')
metadata = MetaData()

offices = Table('offices', metadata,
        Column('officeCode', String(10), primary_key=True),
        Column('city', String(50), nullable=False),
        Column('phone', String(50), nullable=False, unique=True),
        Column('addressLine1', String(50), nullable=False),
        Column('addressLine2', String(50)),
        Column('state', String(50)),
        Column('country', String(50), nullable=False),
        Column('postalCode', String(15), nullable=False),
        Column('territory', String(10), nullable=False)
)

employees = Table('employees', metadata,
        Column('employeeNumber', Integer, primary_key=True),    # this make the field auto-incremented automatically in table structure
        Column('lastName', String(50), nullable=False),
        Column('firstName', String(50), nullable=False),
        Column('extension', String(10), nullable=False),
        Column('email', String(100), nullable=False, unique=True),                               # I make it unique
        Column('officeCode', String(10), ForeignKey('offices.officeCode'), nullable=False,),
        Column('reportsTo', Integer, ForeignKey('employees.employeeNumber')),
        Column('jobTitle', String(50), nullable=False)
)

customers = Table('customers', metadata,
        Column('customerNumber', Integer, primary_key=True),             # this make the field auto-incremented automatically in table structure
        Column('customerName', String(50), nullable=False),
        Column('contactLastName', String(50), nullable=False),
        Column('contactFirstName', String(50), nullable=False),
        Column('phone', String(50), nullable=False, unique=True),                               # I make it unique
        Column('addressLine1', String(50), nullable=False),
        Column('addressLine2', String(50)),
        Column('city', String(50), nullable=False),
        Column('state', String(50)),
        Column('postalCode', String(15)),
        Column('country', String(50), nullable=False),
        Column('salesRepEmployeeNumber', Integer, ForeignKey('employees.employeeNumber')),
        Column('creditLimit', Numeric(10,2))
)

payments = Table('payments', metadata,
        Column('customerNumber', Integer, ForeignKey('customers.customerNumber'), primary_key=True,),
        Column('checkNumber', String(50), nullable=False, primary_key=True),
        Column('paymentDate', Date, nullable=False),
        Column('amount', Numeric(10,2), nullable=False),
)

orders = Table('orders', metadata,
        Column('orderNumber', Integer, primary_key=True),
        Column('orderDate', Date, nullable=False),
        Column('requiredDate', Date, nullable=False),
        Column('shippedDate', Date),
        Column('status', String(15), nullable=False),           # this should be like schedule with many options by default, in other table
        Column('comments', String(500)),
        Column('customerNumber', Integer, ForeignKey('customers.customerNumber'), nullable=False,)
)

orderdetails = Table('orderdetails', metadata,
        Column('orderNumber', Integer, ForeignKey('orders.orderNumber'), primary_key=True),
        Column('productCode', String(15), ForeignKey('products.productCode'), nullable=False, primary_key=True),
        Column('quantityOrdered', Integer, nullable=False),
        Column('priceEach', Numeric(10,2), nullable=False),
        Column('orderLineNumber', SmallInteger, nullable=False)
)

productlines = Table('productlines', metadata,
        Column('productLine', String(50), primary_key=True),
        Column('textDescription', String(4000)),
        Column('htmlDescription', String(200)),                        # this should be validated to real html path
        Column('image', Binary)                                   # what extension is here....????
)

products = Table('products', metadata,
        Column('productCode', String(15), primary_key=True),
        Column('productName', String(70), nullable=False),
        Column('productLine', String(50), ForeignKey('productlines.productLine'), nullable=False),
        Column('productScale', String(10), nullable=False),
        Column('productVendor', String(50), nullable=False),
        Column('productDescription', String(500), nullable=False),
        Column('quantityInStock', SmallInteger, nullable=False),
        Column('buyPrice', Numeric(10,2), nullable=False),
        Column('MSRP', Numeric(10,2), nullable=False),
        CheckConstraint('quantityInStock >= 0', name='quantityInStock_positive')        # I am ensuring that quantityInStock data is always positive
)

metadata.create_all(engine)     #The create_all() function uses the engine object to create all the defined table objects and stores the information in metadata.
# print(repr(<table_name>))     #Print by console the created table

