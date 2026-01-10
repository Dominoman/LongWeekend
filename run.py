from app import create_app, db
from flask_migrate import Migrate
from app import models
from app.models import Search,Itinerary,Route

app = create_app()
migrate = Migrate(app,db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Search=Search,Itinerary=Itinerary,Route=Route)

if __name__=='__main__':
    app.run(debug=True)
