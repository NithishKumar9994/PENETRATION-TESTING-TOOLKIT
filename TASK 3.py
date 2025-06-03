import socket
import requests
import argparse

def scan_ports(target, start_port, end_port):
    print(f"\n🔍 Scanning {target} ports {start_port} to {end_port}...")
    open_ports = []
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"[OPEN] Port {port}")
            open_ports.append(port)
        sock.close()
    if not open_ports:
        print("No open ports found.")
    print("Port scan completed.\n")

def run_bruteforce(url):
    username = input("Enter username: ")
    passwords = ["123456", "password", "admin", "letmein"]  # simple demo list

    print(f"\n🔐 Starting brute-force attack on {url} for user '{username}'")
    for pwd in passwords:
        print(f"Trying password: {pwd}")
        data = {"username": username, "password": pwd}
        try:
            response = requests.post(url, data=data, timeout=5)
            if "invalid" not in response.text.lower():
                print(f"✅ Password found: {pwd}")
                return
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {url}: {e}")
            return
    print("Brute-force complete. Password not found in list.\n")

def grab_banner(ip, port):
    print(f"\n📡 Grabbing banner from {ip}:{port}...")
    try:
        sock = socket.socket()
        sock.settimeout(3)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode().strip()
        print(f"Banner: {banner}\n")
        sock.close()
    except Exception as e:
        print(f"Failed to grab banner: {e}\n")

def select_module_interactive():
    print("Select module to run:")
    print("1. Port Scanner")
    print("2. Brute Forcer")
    print("3. Banner Grabber")
    choice = input("Enter choice (1/2/3): ")
    mapping = {"1": "portscan", "2": "bruteforce", "3": "banner"}
    return mapping.get(choice)

def main():
    parser = argparse.ArgumentParser(description="Modular Penetration Testing Toolkit")
    parser.add_argument("-m", "--module",
                        choices=["portscan", "bruteforce", "banner"],
                        help="Module to run")
    args = parser.parse_args()

    module = args.module
    if not module:
        module = select_module_interactive()
        if not module:
            print("Invalid choice, exiting.")
            return

    if module == "portscan":
        target = input("Target IP/domain: ")
        start_port = int(input("Start port (e.g., 1): "))
        end_port = int(input("End port (e.g., 1024): "))
        scan_ports(target, start_port, end_port)

    elif module == "bruteforce":
        url = input("Target login URL: ")
        run_bruteforce(url)

    elif module == "banner":
        ip = input("Target IP: ")
        port = int(input("Target port: "))
        grab_banner(ip, port)

if __name__ == "__main__":
    main()

from flask import Flask, request, render_template_string

app = Flask(__name__)

login_form = """
<h2>Login Page</h2>
<form method="POST">
  <label>Username:</label><br>
  <input name="username" type="text"><br>
  <label>Password:</label><br>
  <input name="password" type="password"><br>
  <input type="submit" value="Login">
</form>
{% if message %}
<p>{{ message }}</p>
{% endif %}
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "letmein":
            message = "Login successful!"
        else:
            message = "Invalid credentials"
    return render_template_string(login_form, message=message)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80)
