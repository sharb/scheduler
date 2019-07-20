from app import app_instance, configure_routes, api, scheduler


configure_routes(api, scheduler)
# scheduler.start()


app_instance.run(debug=True, host='0.0.0.0', port=8080)

# from app import scheduler

