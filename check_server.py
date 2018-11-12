#! /usr/bin/python3

from app import application
if __name__ == '__main__':

    application.run(debug=True, host='0.0.0.0')


# from flask_restful import Api
# from flask import Flask

# import app.db
# import app.user
# import app.exception


# application = Flask(__name__)
# api = Api(application)


# app.exception.register_exceptions(application)

# app.db.create_db('sqlite:///plat.db?check_same_thread=False')

# app.user.connect(api, '/user')


# if __name__ == '__main__':

#     application.run(debug=True,host='0.0.0.0')
