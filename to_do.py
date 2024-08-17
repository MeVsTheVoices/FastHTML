from fasthtml.common import *

app = FastHTML(hdrs=(picolink))

flexbox_grid = "https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css"

to_dos = []

@app.get("/")
def home():
    return Title("To Do List"), Main(
        Header(Hgroup(H1("To Do List"), H2("Make plans about what to do"))),
        Body(
        Form(
            Input(type="text", name="data"),
            Button("Add", hx_post="/to_do", 
                   hx_target="#to_do_list", hx_swap="innerHTML"),
            role="group"
        ),
        Ul(
            hx_get= "/to_do", hx_swap="innerHTML", 
            hx_target="#to_do_list", hx_trigger="load",
            id="to_do_list",
        ),  
        cls="container"
        )
    )

@app.get("/to_do")
def to_do():
    return Ul(
        *[Li (Span(to_do), 
              Button("Remove", hx_delete=f"/to_do?data={i}", 
                     hx_target="#to_do_list", hx_swap="innerHTML"), 
              id=f"to_do_{i}") for i, to_do in enumerate(to_dos)]
    )

@app.post("/to_do")
def add(data:str):
    to_dos.append(data.capitalize())
    return to_do()

@app.delete("/to_do")
def remove(data:int):
    del to_dos[data]
    return to_do()