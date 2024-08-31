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
                    Ul(
                        id="cidr_form"
                    ),
                    cls="container"
                )
            )

@app.post("/calculate")
def calculate(data:str):
    # convert to bit array
    network_bitarray, host_bits = cidr_to_bitarrays(data)
    print(network_bitarray)
    print(host_bits)
    cidr_check_results = cidr_check(network_bitarray, host_bits)
    if cidr_check_results:
        return Ul(
            Li(cidr_check_results),
            id="cidr_form",
            cls="container"
        )
    # calculate the CIDR notation
    return Ul(
                Li(f"IP address: {data.split('/')[0]}"),
                Li(f"CIDR notation: {data}"),
                Li(f"Number of host bits: {str(32 - int(data.split('/')[1]))}"),
                id="cidr_form",
                cls="container"
            )

def cidr_to_bitarrays(data):
    network, hosts = data.split("/")
    network_bitarray = bitarray.bitarray(''.join([bin(int(x))[2:].zfill(8) for x in network.split('.')]))
    host_bitarray = bitarray.bitarray(''.join(['1' for x in range(0, 32 - int(hosts))]))
    return network_bitarray, host_bitarray

def cidr_check(network_bitarray, host_bitarray):
    padding_length = len(network_bitarray) - len(host_bitarray)
    padded_host_bitarray = bitarray.bitarray('0' * 32)
    padded_host_bitarray |= host_bitarray
    print(padded_host_bitarray)
    print(network_bitarray)
    if padded_host_bitarray & network_bitarray:
        return "Network ID has too many bits set" 
    else:
        return None

def bitarray_to_ip(bits):
    ip_address = '.'.join([str(int(bits[i:i+8].to01(), 2)) for i in range(0, 32, 8)])
