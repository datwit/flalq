#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request, url_for
from api.models.productlines import Productline, ProductlineSchema
from api.utils.database import session, engine
from api.utils import responses as resp
from sqlalchemy import text
from api.config.config import app_config
from werkzeug.utils import secure_filename
import os


productline_routes = Blueprint("productline_routes", __name__)
object_schema = ProductlineSchema()

# UPLOAD_FOLDER = 'C:/Users/Danay/Desktop/danay_python/snippets/api_classic/api/images/'
# ALLOWED_EXTENSIONS = {'png', 'jpg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app_config.ALLOWED_EXTENSIONS

# Create a URL route in our application for "/productlines/" to read a collection
@productline_routes.route('/productlines/', methods=['GET'])
def allproductlines():
    rows = session.query(Productline).all()
    result = object_schema.dump(rows, many=True)
    return resp.response_with(resp.SUCCESS_200, value={"Row List": result}), resp.SUCCESS_200


# Create a URL route in our application for "/productlines/" to create a new row
@productline_routes.route('/productlines/', methods=['POST'])
def postproductline():
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('productLine'):
        found = session.query(Productline).get(data["productLine"])
        if not found:
            try:
                row = object_schema.load(data)
                session.add(row)
                session.commit()
                result = object_schema.dump(session.query(Productline).get(data["productLine"]))
                return resp.response_with(resp.SUCCESS_201, value={"Inserted Data": result}), resp.SUCCESS_201
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "Key data already exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/productlines/" to submit a file picture
@productline_routes.route('/productlines/image/<string:productLine>', methods=['POST'])
def postimageproductline(productLine):
    found = productLine
    file = request.files['image']
    if not file:
        return resp.response_with(resp.INVALID_INPUT_422, value={"error": "No file provided"}), resp.INVALID_INPUT_422
    # if user does not select file, browser also submit an empty part without filename
    elif file.filename == '':
        return resp.response_with(resp.INVALID_INPUT_422, value={"error": "No name data provided"}), resp.INVALID_INPUT_422
    elif file:
        found = session.query(Productline).get(found)
        if found:
            try:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app_config.UPLOAD_FOLDER, filename))
                    found.image = url_for('uploaded_file', filename=filename, _external=True)
                    print(found.image)
                    session.add(found)
                    session.commit()
                    result = object_schema.dump(found)
                    return resp.response_with(resp.SUCCESS_201, value={"Inserted Data Image to": result}), resp.SUCCESS_201
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "Key data already exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/productlines/" to read a particular row in the collection
@productline_routes.route('/productlines/<string:productLine>', methods=['GET'])
def getproductlines(productLine):
    productLine_found = productLine
    found = session.query(Productline).get(productLine_found)
    if not found:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404
    else:
        result = object_schema.dump(found)
        return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200


# Create a URL route in our application for "/productlines/" to update all details of an existing row
@productline_routes.route('/productlines/<string:productLine>', methods=['PUT'])
def putproductlines(productLine):
    productLine_found = productLine
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "No input data provided"}), resp.BAD_REQUEST_400
    elif data.get('productLine'):
        found = session.query(Productline).get(productLine_found)
        if found:
            try:
                row = object_schema.dump(data)
                session.query(Productline).filter(Productline.productLine==productLine_found).update(row)
                session.commit()
                result = object_schema.dump(found)
                return resp.response_with(resp.SUCCESS_200, value={"Updated Row": result}), resp.SUCCESS_200
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "The request data no exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/productlines/" to update some details of an existing row
@productline_routes.route('/productlines/<string:productLine>', methods=['PATCH'])
def patchoffice(productLine):
    productLine_found = productLine
    data = request.get_json()
    if not data:
        return resp.response_with(resp.BAD_REQUEST_400), resp.BAD_REQUEST_400
    elif data.get('productLine'):
        found = session.query(Productline).get(productLine_found)
        if found:
            try:
                if data.get('textDescription'):
                    found.textDescription = data['textDescription']
                if data.get('htmlDescription'):
                    found.htmlDescription = data['htmlDescription']
                session.add(found)
                session.commit()
                result = object_schema.dump(found)
                return resp.response_with(resp.SUCCESS_200, value={"Updated Row Fields": result}), resp.SUCCESS_200
            except Exception as e:
                session.rollback()
                return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
        else:
            return resp.response_with(resp.INVALID_FIELD_NAME_SENT_422, value={"error": "The request data no exists"}), resp.INVALID_FIELD_NAME_SENT_422
    else:
        return resp.response_with(resp.BAD_REQUEST_400, value={"error": "Data no has key field"}), resp.BAD_REQUEST_400


# Create a URL route in our application for "/productlines/" to delete an existing row
@productline_routes.route('/productlines/<string:productLine>', methods=['DELETE'])
def delproductlines(productLine):
    productLine_found = productLine
    found = session.query(Productline).get(productLine_found)
    if found:
        try:
            session.delete(found)
            session.commit()
            return resp.response_with(resp.SUCCESS_204, value={'message': 'Deleted Row'}), resp.SUCCESS_204
        except Exception as e:
            session.rollback()
            return resp.response_with(resp.BAD_REQUEST_400, value={"error": str(e)}), resp.BAD_REQUEST_400
    else:
        return resp.response_with(resp.SERVER_ERROR_404, value={"error": "The request data no exists"}), resp.SERVER_ERROR_404