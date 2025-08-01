def parse_interfaces(raw_status: str):
    lines = raw_status.strip().splitlines()
    data_lines = [line.strip() for line in lines if not line.startswith("Interface")]

    parsed = []
    for line in data_lines:
        parts = line.split()
        if len(parts) >= 6:
            parsed.append(
                {
                    "interface": parts[0],
                    "ip": parts[1],
                    "ok": parts[2],
                    "method": parts[3],
                    "status": parts[4],
                    "protocol": parts[5],
                }
            )
    return parsed
