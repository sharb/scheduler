# from app import app, configure_routes, api, scheduler, logging
from app import app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
