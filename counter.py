from fasthtml.common import *

app = FastHTML(hdrs=(picolink))

count = 0

@app.get("/")
def home():
    return Title("Count Demo"), Main(
        H1("Count Demo"),
        Form(
            Input(type="number", name="data"),
            Button("Set", hx_post="/set", hx_target="#count", hx_swap="innerHTML")
        ),
        P(f"Count is set to {count}", id="count"),
        Button("Increment", hx_post="/increment", hx_target="#count", hx_swap="innerHTML"),
        Button("Decrement", hx_post="/decrement", hx_target="#count", hx_swap="innerHTML"),
        cls="container"
    )

@app.post("/set")
def set_count(data:str):
    global count
    count = int(data)
    return f"Count is set to {count}"

@app.post("/increment")
def increment():
    global count
    count += 1
    return f"Count is set to {count}"

@app.post("/decrement")
def decrement():
    global count
    count -= 1
    return f"Count is set to {count}"