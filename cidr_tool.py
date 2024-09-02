import bitarray.util
from fasthtml.common import *

app = FastHTML(hdrs=(picolink))

import bitarray

@app.get("/")
def home():
    return Title("CIDR calculator"), Main(
                Header(Hgroup(H1("CIDR calculator"), H2("Calculate the CIDR notation of an IP address"))),
                Body(
                    Form(
                        Input(type="text", name="data"),
                        Button("Calculate", hx_post="/calculate", 
                               hx_target="#cidr_form", hx_swap="outerHTML"),
                        role="group"
                    ),
                    Form(
                        Div(Label("Range"), Input(id="output_range")),
                        Div(Label("Network"), Input(id="output_broadcast")),
                        Div(Label("Broadcast"), Input(id="output_broadcast")),
                        role="group",
                        id="cidr_form"
                    ),
                    cls="container"
                )
            )

@app.post("/calculate")
def calculate(data:str):
    # convert to bit array
    network_bitarray, host_bitarray = cidr_to_bitarrays(data)
    errors = cidr_check(network_bitarray, host_bitarray)
    print(network_bitarray)
    print(host_bitarray)
    print(errors)
    if not errors:
    #if not cidr_check_results:
        return Form(
                    Div(Label("Range"), Input(str(bitarray.util.ba2int(host_bitarray) - 2), id="output_range")),
                    Div(Label("Network"), Input(bitarray_to_ip(network_bitarray), id="output_broadcast")),
                    Div(Label("Broadcast"), Input(bitarray_to_ip(network_bitarray | host_bitarray), id="output_broadcast")),
                    role="group",
                    id="cidr_form"
                )
    else:
        return Form(
                    Div(Label("Error"), Output(errors, id="output_error")),
                    role="group",
                    id="cidr_form"
                )


def cidr_to_bitarrays(data):
    network, hosts = data.split("/")
    network_bitarray = bitarray.bitarray(''.join([bin(int(x))[2:].zfill(8) for x in network.split('.')]))
    host_bitarray = bitarray.bitarray(''.join(['1' for x in range(0, 32 - int(hosts))]))
    hosts_padding_length = len(network_bitarray) - len(host_bitarray)
    host_bitarray= bitarray.bitarray('0' * hosts_padding_length) + host_bitarray
    return network_bitarray, host_bitarray

def cidr_check(network_bitarray, host_bitarray):
    return None

def bitarray_to_ip(bits):
    return '.'.join([str(int(bits[i:i+8].to01(), 2)) for i in range(0, 32, 8)])
