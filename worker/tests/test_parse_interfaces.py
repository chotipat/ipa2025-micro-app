from worker.parser import parse_interfaces

def test_parse_interfaces():
    raw_output = """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.1.1     YES manual up                    up      
GigabitEthernet0/1     unassigned      YES unset  administratively down down    
"""
    expected = [
        {
            "interface": "GigabitEthernet0/0",
            "ip": "192.168.1.1",
            "ok": "YES",
            "method": "manual",
            "status": "up",
            "protocol": "up"
        },
        {
            "interface": "GigabitEthernet0/1",
            "ip": "unassigned",
            "ok": "YES",
            "method": "unset",
            "status": "administratively",
            "protocol": "down"
        }
    ]

    result = parse_interfaces(raw_output)
    assert result == expected
