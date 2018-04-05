#adapted from https://github.com/miguelgrinberg/Flask-SocketIO/tree/master/example

from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)
thread = None
thread_lock = Lock() #we'll use this lock to prevent multiple clients from modifying thread at the same time

@socketio.on('connect') #run this when the connection starts
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('start', 'connected')
    
def background_thread():
    #this function does the counting
    count = 0
    while true:
        socketio.sleep(5)
        count += 1
        emit('my_respose', count) #send count to all clients

@app.route('/')
def index():
    return render_template('home.html', async_mode=socketio.async_mode)

if __name__ == '__main__':
    socketio.run(app, debug=True)
