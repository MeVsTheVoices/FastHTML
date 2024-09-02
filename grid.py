from fasthtml.common import *
import os

app = FastHTML(hdrs=(picolink))

grid_template = '''
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr; 
    grid-column-gap: 20px; 
    grid-row-gap: 20px; 
    justify-items: center; 
    align-items: stretch; 
    transition: opacity 0.5s ease-in;
'''

directory_path = 'static/Lewis/'

all_items = os.listdir(directory_path)
all_items.sort()
all_items = [f'{directory_path}{item}' for item in all_items]
all_items = [item for item in all_items if item.endswith('.jpg')]

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
                *get_row(0),
                style=grid_template,
            ),
            cls='container'
        ),
        Style(
            """
            img {
                width: 100%;
                height: 100%;
                object-fit: contain;
                background-color: transparent;
                opacity: 1;
                transition: opacity 0.5s ease-in;
            }
            img.htmx-added {
                opacity: 0;
            }
            """
            
        )
    )

def get_row(number:int):
    return [Img(
                src=all_items[number]) 
                for number in range(number * 4, number * 4 + 3)] + [
            Img(src=all_items[number],
                hx_trigger="revealed",
                hx_get=f"/grid?number={number + 1}",
                hx_swap="afterend settle:1s")]

@app.get('/grid')
def grid(number:int):
    g = get_row(number)
    return (*g,)