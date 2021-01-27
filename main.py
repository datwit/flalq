#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Flask, send_from_directory
from api.utils.database import engine
from api.routes.offices import office_routes
from api.routes.employees import employee_routes
from api.routes.customers import customer_routes
from api.routes.productlines import productline_routes
from api.routes.products import product_routes
from api.routes.orders import order_routes
from api.routes.orderdetails import orderdetail_routes
from api.routes.payments import payment_routes
from api.utils.responses import response_with
from api.utils import responses as resp


app = Flask(__name__)

# Establish the mysql connection
engine.connect()

app.register_blueprint(office_routes)
app.register_blueprint(employee_routes)
app.register_blueprint(customer_routes)
app.register_blueprint(productline_routes)
app.register_blueprint(product_routes)
app.register_blueprint(order_routes)
app.register_blueprint(orderdetail_routes)
app.register_blueprint(payment_routes)

# to restrict file length (response Error: read ECONNRESET, HTTP_413_REQUEST_ENTITY_TOO_LARGE)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024


@app.errorhandler(500)
def handle_app_base_error(e):
    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def handle_object_not_found_error(e):
    return response_with(resp.SERVER_ERROR_404)

@app.errorhandler(400)
def bad_request(e):
    # logging.error(e)
    return response_with(resp.BAD_REQUEST_400)

@app.route('/image/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    app.run(host='localhost', port=4000, debug=True)





