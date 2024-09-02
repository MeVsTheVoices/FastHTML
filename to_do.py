from fasthtml.common import *

app = FastHTML(hdrs=(picolink))

flexbox_grid = "https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css"

to_dos = []

grid_template = '''
        display: grid;
        grid-template-columns: 4fr 1fr;
        grid-column-gap: 20px
        grid-row-gap: 40px
        justify-items: stretch
        align-items: stretch
'''

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
        Div(
            hx_get= "/to_do", hx_swap="innerHTML", 
            hx_target="#to_do_list", hx_trigger="load",
            id="to_do_list", cls="gridded"
        ),  
        cls="container"
        )
    )

@app.get("/to_do")
def to_do():
    return Div(
        *[(Span(to_do), 
              Button("Remove", hx_delete=f"/to_do?data={i}", 
                     hx_target="#to_do_list", hx_swap="innerHTML",
                     style="margin-bottom: 20px;"))
                       for i, to_do in enumerate(to_dos)],
        style=grid_template
    )

@app.post("/to_do")
def add(data:str):
    to_dos.append(data.capitalize())
    return to_do()

@app.delete("/to_do")
def remove(data:int):
    del to_dos[data]
    return to_do()