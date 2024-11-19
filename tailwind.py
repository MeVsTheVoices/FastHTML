from fasthtml.common import *

tailwindlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css", type="text/css")
flowbite = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css", type="text/css")

# Our FastHTML app
app = FastHTML(hdrs=(tailwindlink))

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
def index():
    return Body(
            Nav(
                Div(
                    A("Home", href="/", cls="text-white hover:bg-gray-700 p-4 rounded"),
                    Div(
                Div(
                    Button(
                        "Options",
                        Svg(
                            Path(fill_rule="evenodd", d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z", clip_rule="evenodd"),
                            viewBox="0 0 20 20", 
                            fill="currentColor", 
                            aria_hidden="true", 
                            data_slot="icon",
                            cls="-mr-1 size-5 text-gray-400"
                        ),
                        type="button", 
                        cls="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50", 
                        id="menu-button", 
                        aria_expanded="true", 
                        aria_haspopup="true"
                    )
                ),
                Div(
                    Div(
                        A("Edit", href="#", cls="block px-4 py-2 text-sm text-gray-700", role="menuitem", tabindex="-1", id="menu-item-0"),
                        A("Duplicate", href="#", cls="block px-4 py-2 text-sm text-gray-700", role="menuitem", tabindex="-1", id="menu-item-1"),
                        cls="py-1", role="none"
                    ),
                    Div(
                        A("Archive", href="#", cls="block px-4 py-2 text-sm text-gray-700", role="menuitem", tabindex="-1", id="menu-item-2"),
                        A("Move", href="#", cls="block px-4 py-2 text-sm text-gray-700", role="menuitem", tabindex="-1", id="menu-item-3"),
                        cls="py-1", role="none"
                    ),
                    Div(
                        A("Share", href="#", cls="block px-4 py-2 text-sm text-gray-700", role="menuitem", tabindex="-1", id="menu-item-4"),
                        A("Add to favorites", href="#", cls="block px-4 py-2 text-sm text-gray-700", role="menuitem", tabindex="-1", id="menu-item-5"),
                        cls="py-1", role="none"
                    ),
                    Div(
                        A("Delete", href="#", cls="block px-4 py-2 text-sm text-gray-700", role="menuitem", tabindex="-1", id="menu-item-6"),
                        cls="py-1", role="none"
                    ),
                    cls="absolute right-0 z-10 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black/5 focus:outline-none", 
                    role="menu", 
                    aria_orientation="vertical", 
                    aria_labelledby="menu-button", 
                    tabindex="-1"
                ),
                cls="relative inline-block text-left"
            ),


                    A("Contact", href="/contact", cls="text-white hover:bg-gray-700 p-4 rounded"),
                    cls="flex justify-between items-center h-full w-full p-4"
                ),
                cls="bg-gray-800 w-full h-20 rounded-b-lg",
            ),
            Section(
                cls="bg-gray-200 w-full h-full",
            ),
            Footer(
                cls="bg-gray-600 w-full h-16 rounded-t-lg",
            ),
            cls="flex flex-col h-screen"
        )
