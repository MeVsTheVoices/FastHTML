from fasthtml.common import *
import asyncio
import sys

from enum import Enum
class Headers(Enum):
    FLEXBOX = "https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css"
    HTMX_WS = "https://unpkg.com/htmx-ext-ws@2.0.0/ws.js"
    CSS = Style('''
        body, html { height: 100%; margin: 0; }
        body { display: flex; flex-direction: column; }
        main { flex: 1 0 auto; border: 1px solid black; }
        footer { flex-shrink: 0; padding: 10px; margin: 5px; text-align: center; background-color: #333; color: white; }
        footer a { color: $9cf; }
        #grid { display: grid; grid-template-columns: repeat(20, 20px); grid-template-rows: repeat(20, 20px); gap: 1px; }
        .cell { width: 20px; height: 20px; border: 1px solid black; }
        .alive { background-color: green; }
        .dead { background-color: white; }
    ''')
    PICO = picolink

app = FastHTML(
    headers= (
        Headers.PICO,
        Headers.FLEXBOX,
        Headers.CSS,
        Headers.HTMX_WS
    )
)

game_state = {
    'running' : False,
    'grid' : [[ 0 for _ in range(20) ] for _ in range(20)]
}

def update_grid(grid : list[list[int]]) -> list[list[int]]:
    new_grid = [[ 0 for _ in range(20)] for _ in range(20)]
    def count_neighbors(x, y):
        directions = [(-1, -1), (-1, 0),(-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]): count += grid[nx][ny]
        return count
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            neighbors = count_neighbors(i, j)
            if grid[i][j] == 1:
                if neighbors < 2 or neighbors > 3: new_grid[i][j] = 0
                else: new_grid[i][j] = 1
            elif neighbors == 3: new_grid[i][j] = 1
    return new_grid

def Grid():
    cells = []
    for y, row in enumerate(game_state['grid']):
        for x, cell in enumerate(row):
            cell_class = 'alive' if cell else 'dead'
            cell = Div(
                cls=f'cell {cell_class}',
                hx_put='/update',
                hx_vals={'x': x, 'y': y},
                hx_swap='none',
                hx_target='#gol',
                hx_trigger='click')
            cells.append(cell)
        return Div(*cells, id='grid')
    
def Home():
    gol = Div(Grid(), id='gol', cls='row center-xs')
    run_btw = Button(
        'Run', 
        id = 'run', 
        cls='col-xs-2',
        hx_put='/run',
        hx_target='#gol',
        hx_swap='none')
    pause_btn = Button(
        'Pause',
        id='pause',
        cls='col-xs-2',
        hx_put='/pause',
        hx_swap='none'
    )
    reset_btn = Button(
        'Reset',
        id='reset'
    )