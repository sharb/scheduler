from app import app, configure_routes, api, scheduler, logging


if __name__ == "__main__":
    configure_routes(api, scheduler, logging)
    # scheduler.start()


    app.run(debug=True, host='0.0.0.0', port=80)

    # from app import scheduler

