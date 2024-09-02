from fasthtml.common import *

app = FastHTML(hdrs=(picolink))
# ... other imports and code

@app.get('/')
def index():
    return Html(
        Head(Link(rel="stylesheet", href="https://cdn.jsdelivr.net/flexboxgrid/6.3.1/flexboxgrid.min.css")),
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
