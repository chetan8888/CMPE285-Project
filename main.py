from website import create_app

app = create_app()

if __name__ == '__main__':
    # debug = True means whenever there is a change in the backend code the server should restart
    app.run(debug = True) 