from app import createApp, socketio

app = createApp(debug=True)

if __name__ == '__main__':
    socketio.run(app)
