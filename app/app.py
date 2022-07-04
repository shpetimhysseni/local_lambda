from app.configs.setup_flask import setup_flask_app
import serverless_wsgi


app = setup_flask_app()

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)