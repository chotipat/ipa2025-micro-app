# worker/router_client.py
from netmiko import ConnectHandler


def fetch_interface_status(router_info):
    connection = ConnectHandler(**router_info)
    output = connection.send_command("show ip interface brief")
    connection.disconnect()
    return output
