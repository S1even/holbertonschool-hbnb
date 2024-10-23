from app import create_app
from app.services.facade import HBnBFacade

app = create_app()
facade = HBnBFacade()

if __name__ == '__main__':

    app.run(debug=True)