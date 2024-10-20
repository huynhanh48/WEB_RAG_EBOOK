from flask import Flask
from  app import db,create_app
import os
config_name = os.getenv('FLASK_CONFIG', 'development') 
app = create_app(config_name)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8000',debug=True)
    