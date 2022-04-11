from flask_migrate import Migrate
import os
from src import create_app, db

app = create_app(os.getenv("FLASK_ENV"))
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG"))
