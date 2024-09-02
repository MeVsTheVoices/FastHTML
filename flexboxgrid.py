from fasthtml.common import *

gridlink = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css")

# Our FastHTML app
app = FastHTML(hdrs=(picolink, gridlink))

@app.get('/')
def index():
    return Html(
        Body(
            Div(
                Div(
                    Div(
                        "Hello, World!",
                        cls="box",
                    ),
                    background_color="red",
                    cls="col-xs-12 col-sm-6 col-md-4 col-lg-3",
                ),
                cls="row"
            )
        )
    )


app.mount("/static", StaticFiles(directory="static"), name="static")
