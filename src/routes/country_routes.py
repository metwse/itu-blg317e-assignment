def register_routes(app, country_handler, status_handler):
    app.add_url_rule("/", "status", status_handler.get_status, methods=["GET"])
    app.add_url_rule("/countries", "list_countries", country_handler.list_countries, methods=["GET"])
    app.add_url_rule("/countries/<code>", "get_country", country_handler.get_country, methods=["GET"])
    app.add_url_rule("/countries", "create_country", country_handler.create_country, methods=["POST"])
