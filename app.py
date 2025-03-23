from flask import Flask

app = Flask(__name__)

import config
import controllers.authentication
import controllers.admin_routes
import models

if __name__ == "__main__":
    app.run(debug=True)