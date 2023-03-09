CLUSTER = {"1": 25000, "2": 26000, "3": 27000}


def get_port_number(server_number):
    peers = [value for key, value in CLUSTER.items() if key not in [server_number]]
    return CLUSTER[server_number], peers
