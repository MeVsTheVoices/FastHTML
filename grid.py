from fasthtml.common import *
import os

app = FastHTML(hdrs=(picolink))

grid_template = '''display: grid;grid-template-columns: 1fr 1fr 1fr 1fr; grid-column-gap: 20px; grid-row-gap: 20px; justify-items: center; align-items: stretch;'''

directory_path = 'static/Lewis/'

all_items = os.listdir(directory_path)
all_items.sort()
all_items = [f'{directory_path}{item}' for item in all_items]

app.mount("/static/Lewis", StaticFiles(directory="static/Lewis"), name="static")

@app.get('/')
def index():
    print(all_items)
    return Body(
        Header(
            Hgroup(
                H1('Grid Example'),
                P('This is a simple example of a grid layout using FastHTML.')
            ),
            cls='container'
        ),
        Main(
            Div(
                *[Img(src=item, style='width: 100%; height: 100%; object-fit: cover;') for item in all_items],
                style=grid_template
            ),
            cls='container'
        )
    )

@app.get('/grid?{number:int}')
def grid(number:int):
    return Img(src=all_items[number], style='width: 100%; height: 100%; object-fit: cover;')