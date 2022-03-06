from flask_app import app

from flask_app.controllers import users
# import all controller files here

if __name__=="__main__":    
    app.run(debug=True)