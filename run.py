from app.main import create_app

app = create_app()

if __name__ == "__main__":
    print("Flask is starting ✅")
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
