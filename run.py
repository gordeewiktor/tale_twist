#run.py
from app import create_app, db

app = create_app('development')  # Set to 'development' by default or another suitable configuration

with app.app_context():
    try:
        print("Attempting to create database tables...")
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print("Failed to create database tables:", e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
