from Package import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# will import the app from __init__ file 
