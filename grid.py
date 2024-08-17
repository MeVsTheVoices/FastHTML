from fasthtml.common import *

app = FastHTML(hdrs=(picolink))

@app.route('/'):
def index(req, res):
    res.body = 'Hello, World!'