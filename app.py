from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# GLOBAL STATE
# None = Button is free
# "Name" = Button is locked by that person
locked_by = None


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('user_clicked')
def handle_click(data):
    global locked_by
    name = data.get('name', 'Anonymous')

    # CASE 1: SERGEI CLICKS (The Reset)
    if name == "Sergei":
        locked_by = None
        print("Sergei reset the game.")
        # Broadcast reset to everyone
        emit('game_reset', {'message': 'READY!'}, broadcast=True)
        return

    # CASE 2: NORMAL USER CLICKS
    if locked_by is None:
        # Success! They were first.
        locked_by = name
        print(f"Locked by {name}")
        # Broadcast lock to everyone
        emit('game_locked', {'winner': name}, broadcast=True)
    else:
        # Too late! Button is already locked.
        print(f"{name} clicked too late.")
        # Optional: We could tell this specific user they failed,
        # but the frontend handles the disabled state, so we do nothing.


if __name__ == '__main__':
    # Use 5001 to avoid port conflicts
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)