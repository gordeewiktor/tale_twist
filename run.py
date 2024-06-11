from app import create_app, db

app = create_app('production')  # Set to 'production' for Heroku deployment

with app.app_context():
    try:
        print("Attempting to create database tables...")
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print("Failed to create database tables:", e)

if __name__ == "__main__":
    app.run()
