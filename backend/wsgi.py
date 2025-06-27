from application import create_app

app = create_app()

if __name__ == "__main__":
    host = app.config.get("FLASK_RUN_HOST", "0.0.0.0")
    port = app.config.get("FLASK_RUN_PORT", 5000)
    debug = app.config.get("DEBUG", True)

    app.run(host=host, port=port, debug=debug)
