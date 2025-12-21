from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# Initialize SocketIO
socketio = SocketIO(app)


@app.route('/')
def index():
    # Serve the HTML file
    return render_template('index.html')


# Listen for the 'user_clicked' event from the browser
@socketio.on('user_clicked')
def handle_click(data):
    name = data.get('name', 'Anonymous')
    print(f"Server received click from: {name}")

    # Broadcast a 'update_feed' event to ALL connected clients
    emit('update_feed', {'message': f'{name} just clicked the button!'}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)