from backend import create_app

# Initialize Flask app
app = create_app()

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
