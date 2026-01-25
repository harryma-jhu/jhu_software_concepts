from backbone import create_app
# In __init__.py
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)