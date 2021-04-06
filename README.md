
# API flalq: using Flask and SQLAlchemy

**API flalq** uses the structure from the MySQL Basic [Tutorial]((https://www.mysqltutorial.org/basic-mysql-tutorial.aspx)) database. Developed with **Flask**, **SQLAlchemy** (not Flask_SQLAlchemy), **marshmallow**, **unittest** and **mysql** db. In this case, the application has been built with [SQLAlchemy ORM](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html). Contains different data types and endpoints, trying to cover simple examples that can be useful to other projects.


---
## Index

- [API flalq: using Flask and SQLAlchemy](#api-flalq-using-flask-y-sqlalchemy)
  - [Index](#index)
  - [Requirements](#requirements)
  - [Installation, Configuration and Usage](#installation-configuration-and-usage)
    - [Clone the repository](#clone-the-repository)
    - [Install dependencies](#install-dependencies)
    - [Load the Sample Database into MySQL Server](#load-the-sample-database-into-mysql-server)
    - [Running the aplication](#running-the-aplication)
  - [Contents](#contents)
  - [Inside the aplication for a moment](#inside-the-aplication-for-a-moment)
  - [How to test](#how-to-test)
  - [Building documentation](#building-documentation)
  - [Contact](#contact)
  - [Thanks](#thanks)

---
## Requirements

This project is developed with the Python 3.7 version and requires installing the libraries present in the file `requirements.txt`:
* [**Klask**](http://flask.pocoo.org/) - minimalist framework written in Python that allows you to create web applications quickly and with a minimum number of lines of code.
* [**SQLAlchemy**](https://www.sqlalchemy.org/) - open source SQL toolkit and object relational mapper for the programming language.
* **Marshmallow** ([mashmallow Documentation](http://marshmallow.readthedocs.io/)) - is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native datatypes.
* **marshmallow_sqlalchemy** ([marshmallow_sqlalchemy Documentation](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)) - SQLAlchemy integration with the marshmallow (de)serialization library.
* [**Unittest2**](https://pypi.python.org/pypi/unittest2) - backport of the new features added to the unittest testing framework.


---

## Installation, Configuration and Usage

### Clone the repository

    git clone https://github.com/datwit/flalq.git

    cd flalq


### Install dependencies

Once placed in the directory where you want to work your project, you have the options of:

* Then you can install from the requirements.txt file

        pip install -r requirements.txt

* Or install separately what you need:

        pip install marshmallow_sqlalchemy


### Load the Sample Database into MySQL Server

From the MySQL Tutorial you can download the [mysql basic database](https://sp.mysqltutorial.org/wp-content/uploads/2018/03/mysqlsampledatabase.zip) in a zip file. Then extract the content (mysqlsampledatabase.sql) into a folder. Upload from your MySQL server:

    source c:\temp\mysqlsampledatabase\mysqlsampledatabase.sql


### Running the aplication

Initially I have created 2 separate databases to run in development and testing environments respectively. But this can be done on your terms and reset in the `config.py` file.

Having configured the variable *FLASK_ENV* in development mode in the activate.bat file of the environment as follows.

`set "FLASK_ENV=development"*`

Running on your console:

    python run.py

The tables in the database will be created instantly.


---
## Contents

This is a partial listing of the contents of this project:

- `api/` - package containing the entire application.

- `api/config/` - folder with the config file.

- `api/config/config.py` - file where the basic settings are defined and the working environment is captured to start.

- `api/images/` - folder with image files.

- `api/models/` - files per table, where all the models and schemes of the application are declared.

- `api/routes/` - files per table, where all the views of the application are configured.

- `api/tests/` - files where the main tests to the application are built.

- `api/utils/` - folder with common functions.

- `api/utils/database.py` - file where the instances and database connection are created.

- `api/utils/responses.py` - utility file to status codes for the responses.

- `api/utils/test_base.py` - file where the application for testing is created.

- `docs/` - contains the documentation files.

- `main.py` - contains all the logic of the application: initializes the app, views, swagger ui and creates the tables in the database.

- `README.md` - this file in markdown format.

- `Requirements.txt` - file that contains all the Python dependencies of the project.

- `run.py` - entry point file to the application. In it, the application is created.

- `.gitignore` - file that defines the directories and files that should not be taken into account by Git.


---
## Inside the aplication for a moment

This is a small piece of code from an endpoint:

    @office_routes.route('/offices/<string:officeCode>', methods=['GET'])
    def getoffice(officeCode):
        officeCode_found = officeCode
        found = session.query(Office).get(officeCode_found)
        if not found:
            return resp.response_with(resp.SERVER_ERROR_404, value={"error": "Key data not exists"}), resp.SERVER_ERROR_404
        else:
            result = object_schema.dump(found)
            return resp.response_with(resp.SUCCESS_200, value={"Request": result}), resp.SUCCESS_200

To add data, for example an office, the query would be as follows:

    {
        "employeeNumber": 2,
        "lastName": "Employee",
        "firstName": "Second",
        "extension": "1000",
        "email": "sales@yahoo.es",
        "officeCode": "OF1",
        "reportsTo": 1,
        "jobTitle": "Shopman"
    }

And swagger ui looks like this:

![Swagger UI](\api\images\swagger_ui.gif "Swagger UI")

A query / response from the web could be like this:

![Web response](\api\images\web_response.gif "Web response")

---
## How to test

First, set *FLASK_ENV* in test mode:

`set "FLASK_ENV=testing"*`

Then, run each unit test as follows :

    python -m unittest api/tests/offices.py

In this project has been used **Coverage** ([Coverage Documentation](https://coverage.readthedocs.io/en/coverage-5.5/)) too. It monitors the program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not. Coverage measurement is typically used to gauge the effectiveness of tests. It can show which parts of your code are being exercised by tests, and which are not.

You can install Coverage in the usual ways. The simplest way is:

    pip install coverage

And run for tests, with unittest in this case:

    coverage run -m unittest api/tests/offices.py

Then to see the results table:

    coverage report -m api/tests/offices.py

But there is another way to show this result and it is the html report:

    coverage html api/tests/offices.py

It should look like this:

![Coverage html Report](\api\images\coverage_html_report.gif "Coverage html Report")


---
## Building documentation

The following was required to build the documentation:
* [**flask_swagger**](https://pypi.org/project/flask-swagger/) - provides a method that inspects the Flask app for endpoints that contain YAML docstrings with Swagger 2.0 Operation objects.
* [**flask_swagger_ui**](https://pypi.org/project/flask-swagger-ui/) - simple Flask blueprint for adding Swagger UI to your flask application, for live interactive documentation.
* [**Markdown**](https://www.fullstackpython.com/markdown.html) - lightweight markup language that allows fast writing of texts.

---
## Contact

Danay Meneses Abad danaymeneses@gmail.com

---
## Thanks

I want to thank, first of all, this entire community of coders (beginners or experienced) who, in addition to their jobs, make videos, tutorials and blogs to share their knowledge and efforts. You can never predict how much one very little thing can help a totally unknown person who is breathing miles away ... and years ... from you !!! Thanks to my brother and instructor (Abel Meneses Abad) for encouraging me to take the first step and believe that I could write some useful code. Thanks to my husband for supporting me.
