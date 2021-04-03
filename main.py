#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
To initialize the app object
"""

from flask import Flask, send_from_directory
from api.utils.database import engine, Base
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
from api.utils.database import session


def create_app(app_config):
    """Create 'app' object, that is a Flask class instance."""
    # The first argument is the name of the application’s module or package. We are using a single module, then we use __name__ argument to initialize our application.
    app = Flask(__name__)
    app.config.from_object(app_config)

    with app.app_context():
        """Create all tables, once the tables have been defined."""
        # Each table object are members of the 'metadata' attribute of declarative 'base' class."""
        Base.metadata.create_all(engine)

    # Register all routes Blueprint in the app
    app.register_blueprint(office_routes)
    app.register_blueprint(employee_routes)
    app.register_blueprint(customer_routes)
    app.register_blueprint(productline_routes)
    app.register_blueprint(product_routes)
    app.register_blueprint(order_routes)
    app.register_blueprint(orderdetail_routes)
    app.register_blueprint(payment_routes)

    # GLOBAL HTTP CONFIGURATIONS
    @app.errorhandler(500)
    def handle_app_base_error(e):
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(404)
    def handle_object_not_found_error(e):
        return response_with(resp.SERVER_ERROR_404)

    @app.errorhandler(400)
    def bad_request(e):
        return response_with(resp.BAD_REQUEST_400)

    @app.route('/image/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

    return app