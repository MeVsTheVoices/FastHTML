from fasthtml.common import *

gridlink = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css")
stylelink = Link(rel="stylesheet", href="/static/buttons.css", type="text/css")

styles = Style(
'''
    .gridded {
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        grid-template-rows: repeat(10, 1fr);
        gap: 2px;
    }
    .cell {
        width: 50px;
        height: 50px;
        border: 1px solid black;
    }
    .cell.toggled {
        background-color: black;
    }
'''
)
# Our FastHTML app
app = FastHTML(hdrs=(picolink, gridlink))


grid_elements_tall = 10
grid_elements_wide = 10
grid_elements = [
    [False for _ in range(grid_elements_tall)] for _ in range(grid_elements_wide)]


@app.get('/')
def index():
    return Body(
            Header(
                Hgroup
                (
                    H1("Conway's Game of Life"),
                    H2("A simulation of cellular automata"),
                ),
            ),
            Div(hx_get="/game_board", hx_trigger="load", cls="gridded"),
            cls="container",
        )

@app.get("/game_board")
def game_board():

    return Div(
        *[Div(
            hx_get=f"/game?rows={a}&cols={b}",
            hx_trigger="click, every 5s",
            hx_target="this",
            cls="cell toggled",)
            for a in range (grid_elements_tall) for b in range(grid_elements_wide)
        ],
    )

@app.get("/game")
def game(rows: int, cols: int):
    is_toggled = grid_elements[rows][cols]
    if is_toggled:
        return Div(cls="cell toggled")
    else:
        return Div(cls="cell")

@app.post('/game')
def updateElement(row : int, col : int):
    grid_elements[row][col] = not grid_elements[row][col]
    


app.mount("/static", StaticFiles(directory="static"), name="static")
