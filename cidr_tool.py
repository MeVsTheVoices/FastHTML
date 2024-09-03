import bitarray.util
from fasthtml.common import *

import re

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
                    build_response("", "", "", ""),
                    cls="container"
                )
            )

@app.post("/calculate")
def calculate(data:str):
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$", data):
        return build_error("Invalid CIDR notation")
    match = re.findall(r"(\d{1,3})", data)
    if any([int(x) > 255 for x in match]):
        return build_error("Invalid IP address")
        if any([int(x) > 255 for x in match]):
            return build_error("Invalid IP address")
        

    network_bitarray, host_bitarray = cidr_to_bitarrays(data)
    network_ip, broadcast_ip, subnet_mask = calculate_ips(network_bitarray, host_bitarray)
    errors = cidr_check(network_bitarray, host_bitarray)
    if not errors:
        return build_response(
            f"{(bitarray.util.ba2int(host_bitarray) - 2):,}", 
            bitarray_to_ip(network_ip), 
            bitarray_to_ip(broadcast_ip),
            bitarray_to_ip(subnet_mask))
    else:
        return Form(
                    Div(Label("Error"), Output(errors, id="output_error")),
                    role="group",
                    id="cidr_form"
                )

def build_response(range: str, network: str, broadcast: str, subnet_mask: str) -> Form:
    return Form(
                Div(Label("Hosts"), Input(value=range, id="output_range", readonly=True)),
                Div(Label("Network"), Input(value=network, id="output_broadcast", readonly=True)),
                Div(Label("Broadcast"), Input(value=broadcast, id="output_broadcast", readonly=True)),
                Div(Label("Subnet Mask"), Input(value=subnet_mask, id="output_subnet_mask", readonly=True)),
                role="group",
                id="cidr_form"
            )
def build_error(error: str) -> Form:
    return Blockquote(error, id="cidr_form")

def cidr_to_bitarrays(data):
    network, hosts = data.split("/")
    network_bitarray = bitarray.bitarray(''.join([bin(int(x))[2:].zfill(8) for x in network.split('.')]))

    host_bitarray = bitarray.bitarray(''.join(['1' for x in range(0, 32 - int(hosts))]))
    hosts_padding_length = len(network_bitarray) - len(host_bitarray)
    host_bitarray = bitarray.bitarray('0' * hosts_padding_length) + host_bitarray

    return network_bitarray, host_bitarray

def calculate_ips(network_bitarray, host_bitarray):
    inverted_host_bitarray = host_bitarray.copy()
    inverted_host_bitarray.invert()
    network_ip = network_bitarray & inverted_host_bitarray
    broadcast_ip = network_ip | host_bitarray

    return network_ip, broadcast_ip, inverted_host_bitarray

def cidr_check(network_bitarray, host_bitarray):
    return None

def bitarray_to_ip(bits):
    return '.'.join([str(int(bits[i:i+8].to01(), 2)) for i in range(0, 32, 8)])
