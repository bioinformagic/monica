from flask import Flask, render_template
from flask_socketio import SocketIO
import libs.experiment as exp

app = Flask(__name__)
socketio = SocketIO(app)

def common_names_generator():
    """
    de-pickles the list of common names from refseq db and feeds it to the starting page as a list
    :return:
    """
    pass


@app.route('/')
def index():
    """
    serves the startpage_index.html
    """
    data = exp.common_names_generator()
    return render_template('startpage_index.html', data=data)