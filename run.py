from app import app_instance, configure_routes, api

configure_routes(api)

app_instance.run(debug=True, host='0.0.0.0', port=8080)