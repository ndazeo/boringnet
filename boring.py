#!/usr/bin/env python3
from posixpath import abspath, dirname
import signal
import threading
import yaml

from subprocess import Popen, TimeoutExpired


def parse_yaml(yaml_file):
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    for key, value in data.items():
        line = "ssh -nNT "
        if "IP" in value:
            if "User" in value:
                line += value.get('User') + "@"
            line += value.get('IP')
        else:
            raise Exception("Missing IP for host: " + key)
        
        if "Port" in value:
            line += " -p " + str(value.get('Port'))

        if "IdentityFile" in value:
            line += " -i " + value.get('IdentityFile')

        if "Tunnels" in value:
            for tunnel in value.get('Tunnels'):
                if not "Remote" in tunnel:
                    raise Exception("Missing Remote for tunnel: " + str(tunnel))
                remote = tunnel.get('Remote')
                if not "Ports" in tunnel:
                    raise Exception("Missing Ports for tunnel: " + str(tunnel))
                ports = tunnel.get('Ports')
                for port in ports:
                    # Check if port is number
                    if isinstance(port, int):
                        line += f" -L {port}:{remote}:{port}"
                    elif len(port.split(":")) == 2:
                        local_port, remote_port = port.split(":")
                        line += f" -L {local_port}:{remote}:{remote_port}"
        yield line

running = True

def start_tunnel(cmd: str):
    global running
    p = Popen(cmd.split(" "))
    while True:
        try:
            p.wait(1000)
            p = Popen(command.split(" "))
        except TimeoutExpired as _e:
            if not running:
                p.kill()
                break
            continue

def signal_handler(sig, frame):
    global running
    running = False

def run():
    print("Starting...")
    signal.signal(signal.SIGINT, signal_handler)
    threads = []
    path = dirname(abspath(__file__))
    for command in parse_yaml(f"{path}/config.yml"):
        t = threading.Thread(target=start_tunnel, args=(command,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("Sopped.")

def test_config():
    path = dirname(abspath(__file__))
    for command in parse_yaml(f"{path}/config.yml"):
        print(command)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_config()
    else:
        run()