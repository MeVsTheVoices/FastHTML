from fasthtml.common import *

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import threading
import time  # Import the time module

app = FastHTML(hdrs=(picolink))

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
        return Title("Matplotlib Demo"), Main(
        H1("Matplotlib Demo"),
        
        # Sliders for parameters
        Div(
            Label("Amplitude:", htmlFor="amplitude"),
            Input(type="range", min="0.1", max="2", step="0.1", value="1", id="amplitude",),
            Br(),
            Label("Frequency:", htmlFor="frequency"),
            Input(type="range", min="0.1", max="3", step="0.1", value="1", id="frequency"),
            Br(),
            Label("Phase:", htmlFor="phase"),
            Input(type="range", min="0", max="6.28", step="0.1", value="0", id="phase"),
        ),

        Button("Plot", 
               hx_post="/plot", 
               hx_target="#plot",
               hx_vars="js:{amplitude:amplitude.value, frequency:frequency.value, phase:phase.value}",
               hx_trigger="click",
               hx_swap="outerHTML"),
        Img(id="plot", src="static/plot.png", alt="Plot", width="500", height="300"),
        cls="container"
    )

def plot_function(x, amplitude=1, frequency=1, phase=0):
    return amplitude * np.sin(frequency * x + phase)


def generate_plot(amplitude: float, frequency: float, phase: float):
    x = np.linspace(start=-10, stop=10, num=100)
    y = plot_function(x, amplitude, frequency, phase)
    plt.plot(x, y)
    plt.savefig("static/plot.png")
    plt.close()

@app.post("/plot")
async def plot(amplitude: float = 1, frequency: float = 1, phase: float = 0):
    plot_thread = threading.Thread(target=generate_plot, args=(amplitude, frequency, phase))
    plot_thread.start()
    plot_thread.join()

    time.sleep(0.1)  

    return Img(id="plot", src=f"static/plot.png?t={int(time.time())}")  

