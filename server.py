from flask_cors import CORS

if __name__ == '__main__':
    from app import create_app

    app = create_app()
    CORS(app, supports_credentials=True) 
    app.run(debug=True, host="0.0.0.0", port=3000)