import tkinter as tk
from tkinter import simpledialog
from tkinter import Canvas
from tkinter import Button
from tkinter import Toplevel
#from tkinter import *
import subprocess
import signal
import os
import sys
import json
import webbrowser
from urllib.parse import urlparse
from tkinter import PhotoImage


class PulseChainLive:
    def __init__(self):
        root = tk.Tk()
        title = "PulseChain Live"
        root.title(title)
        root.geometry("600x550")

        # Get the directory of the script
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Load the image file using the absolute path
        image_path = os.path.join(script_directory, "assets/background.png")
        try:
            background_image = PhotoImage(file=image_path)
        except Exception as e:
            print(f"Background image failed to load: {e}")
            return

        # Create Canvas
        canvas1 = Canvas(root, width = 200, height = 150)

        canvas1.pack(fill = "both", expand = False)

        # Display image
        canvas1.create_image(0, 0, image = background_image, anchor = "nw")

        # Add Text
        canvas1.create_text( 300, 80, text = title, fill="black", font=("Helvetica", 40, 'bold'))
        canvas1.create_text( 305, 85, text = title, fill="#9b7649", font=("Helvetica", 40, 'bold'))


         # Create a button for help
        #help_button = Button(root, text="HELP", command=self.show_help)
        #help_button.pack(pady=10)
        #help_button_canvas = canvas1.create_window(10, 10, anchor = "nw", window = help_button)

        # Create Buttons
        #button1 = Button(root, text = "HELP")
        #button1_canvas = canvas1.create_window(10, 10, anchor = "nw", window = button1)
        #button2 = Button(root, text = "CONFIG")

        # Display Buttons
        #button2_canvas = canvas1.create_window(10, 40, anchor = "nw", window = button2)


        self.scripts = {
            "hex-server": {
		"display_name": "Hex Server",
		"command": "hex-server/hex-server",
		"is_running": False,
		"process": None, 
		"pid": None,
		"url": "http://127.0.0.1:5555/#/",
		"code": "https://gitlab.com/pulsechaincom/hex-server.git"
	    },
            "ethhex-uniswap-server": {
		"display_name": "EthHex Server", 
		"command": "ethhex-uniswap-server/ethhex-uniswap-server", 
		"is_running": False, 
		"process": None, 
		"pid": None, 
		"url": "http://127.0.0.1:5556/#/", 
		"code": "https://gitlab.com/pulsechaincom/ethhex-uniswap-server.git"
	    },
            "pulsex-server": {
		"display_name": "Pulsex Server", 
		"command": "pulsex-server/pulsex-server", 
		"is_running": False, 
		"process": None, 
		"pid": None, 
		"url": "http://127.0.0.1:3691/#/", 
		"code": "https://gitlab.com/pulsechaincom/pulsex-server.git"
	    },
            "pulsechain-bridge-server": {
		"display_name": "Pulsechain Bridge Server", 
		"command": "pulsechain-bridge-server/pulsechain-bridge-server", 
		"is_running": False, 
		"process": None, 
		"pid": None, 
		"url": "http://127.0.0.1:3692/#/", 
		"code": "https://gitlab.com/pulsechaincom/pulsechain-bridge-server.git"
	    },
            "pulsechain-staking-launchpad-server": {
		"display_name": "Pulsechain Staking Server", 
		"command": "pulsechain-staking-launchpad-server/pulsechain-staking-launchpad-server", 
		"is_running": False, 
		"process": None, 
		"pid": None, 
		"url": "http://127.0.0.1:3693/#/", 
		"code": "https://gitlab.com/pulsechaincom/pulsechain-staking-launchpad-server.git"
	    },
            "pulsechain-explorer-server": {
		"display_name": "Pulsechain Explorer Server", 
		"command": "pulsechain-explorer-server/pulsechain-explorer-server", 
		"is_running": False, 
		"process": None, 
		"pid": None, 
		"url": "http://127.0.0.1:3694/#/", 
		"code": "https://gitlab.com/pulsechaincom/pulsechain-explorer-server.git"
	    },
            #"dexscreener": {"display_name": "Dexscreener", "command": "chromium https://dexscreener.com/", "is_running": False, "process": None, "pid": None, "url": "https://dexscreener.com/", "code": ""},
            #"tradingview": {"display_name": "Tradingview", "command": "chromium https://www.tradingview.com/chart/VHTWsltR/", "is_running": False, "process": None, "pid": None, "url": "https://www.tradingview.com/chart/VHTWsltR/", "code": ""},
        }

        self.check_existing_processes()
        max_length = max(len(script_info["display_name"]) for script_info in self.scripts.values())

        for script_name, script_info in self.scripts.items():

            script_code = script_info.get("code", "")  # Assuming script code is stored in a "code" key

            script_frame = tk.Frame(root)
            script_frame.pack(pady=10, padx=3, anchor=tk.W)

            name_label = tk.Label(script_frame, text=f"{script_info['display_name']}: ", width=max_length + 0, anchor=tk.W)
            name_label.pack(side=tk.LEFT, padx=(0, 10))

            start_button = tk.Button(script_frame, text="Start", command=lambda s=script_name: self.start_script(s), state=tk.NORMAL)
            start_button.pack(side=tk.LEFT)
            script_info["start_button"] = start_button

            if not os.path.exists(script_info["command"]):
                start_button.config(state=tk.DISABLED)

            stop_button = tk.Button(script_frame, text="Stop", command=lambda s=script_name: self.stop_script(s), state=tk.DISABLED)
            stop_button.pack(side=tk.LEFT)
            script_info["stop_button"] = stop_button

            if script_info["code"].strip():
                compile_button = tk.Button(script_frame, text="Compile", command=lambda s=script_name, sc=script_code: self.compile_configuration(s, sc))
                compile_button.pack(side=tk.LEFT, padx=0)
                script_info["config_button"] = compile_button

                #compile_button.config(state=tk.DISABLED)

            status_dot = tk.Canvas(script_frame, width=20, height=20)
            status_dot.pack(side=tk.LEFT, padx=(10, 0))
            script_info["status_dot"] = status_dot

            parsed_url = urlparse(script_info["url"])
            port_number = parsed_url.port

            if port_number is None:
                parsed_url = urlparse(script_info["url"])
                domain_parts = parsed_url.netloc.split('.')
                cleaned_domain = '.'.join(domain_parts[-2:])

                print(f"Port number is not specified in the URL, using Domain {cleaned_domain}")

                link_label_text = f"{'Open' if script_info['is_running'] else ''}{cleaned_domain}"

                link_label = tk.Label(script_frame, text=link_label_text, fg="blue", cursor="hand2")
                link_label.pack(side=tk.LEFT)
                link_label.bind("<Button-1>", lambda event, url=script_info["url"]: self.open_browser(event, url))

                # Add the label
                script_info["link_label"] = link_label

            else:
                # Continue with the port_number
                print(f"Port number is {port_number}")

                link_label_text = f"{'Open' if script_info['is_running'] else 'Closed'}: {port_number}"

                link_label = tk.Label(script_frame, text=link_label_text, fg="blue", cursor="hand2")
                link_label.pack(side=tk.LEFT)
                link_label.bind("<Button-1>", lambda event, url=script_info["url"]: self.open_browser(event, url))

                    #link_label = tk.Label(script_frame, text=link_label_text, fg="blue")
                    #liink_label = tk.Label(script_frame, text=link_label_text)
                link_label.pack(side=tk.LEFT)

                script_info["link_label"] = link_label

#            script_info["config_label"] = tk.Label(self.root, text=f"Configuration for {script_info['display_name']}: Not configured")
#            script_info["config_label"].pack_forget()

            if script_info["is_running"]:
                script_info["status_dot"].config(state=tk.NORMAL)
                self.draw_dot(script_info["status_dot"], "green")
                stop_button.config(state=tk.NORMAL)
                start_button.config(state=tk.DISABLED)
            else:
                script_info["status_dot"].config(state=tk.DISABLED)
                self.draw_dot(script_info["status_dot"], "red")
                stop_button.config(state=tk.DISABLED)
                #start_button.config(state=tk.NORMAL)

        root.mainloop()


    def show_help(self):
        # Create a new window for help
        help_window = Toplevel(self.root)
        help_window.title("Help")

        # Add content to the help window
        help_label = tk.Label(help_window, text="This is the help content.")
        help_label.pack(padx=20, pady=20)

        # You can add more widgets and information to the help window

    def toggle_config_area(self, script_name):
        script_info = self.scripts[script_name]
        config_value = script_info.get("config_entry_value", "")
        self.config_label.config(text=f"Configuration Area for {script_info['display_name']}: {config_value}")

    def compile_configuration(self, script_name, script_code):

        # Get the directory path of the script
        #script_directory = os.path.dirname(os.path.abspath(self.scripts[script_name]["command"]))
        #command = f"cd {script_directory}"
        #result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
        #print(result.stdout)

        current_directory = os.getcwd()
        print("Directory (startup):", current_directory)

        if not os.path.exists(f"{script_name}/"):
            print("Server Code Missing")
            command = f"git clone {script_code}"
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
            print(result.stdout)

            #sys.exit()
            os.chdir(script_name)

        else:
            print("Server Code Pull")
            os.chdir(script_name)

            command = f"git pull"
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
            print(result.stdout)


        # Change directory to server working directory.
        current_directory = os.getcwd()
        print("Directory (current):", current_directory)

        #command = f"~/workspace/golang/go/bin/go version"
        command = f"~/workspace/golang/go/bin/go build -o {script_name} ./cmd/{script_name}/main.go"
        #command = f"go build -o {script_name} ./cmd/{script_name}/main.go"
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
        print(f"Output:")
        print(f"{result.stdout}\n")
        print(f"Errors:")
        print(f"{result.stderr}\n")
        print(f"Compiled!!")

        # Change directory back to root.
        os.chdir("../")
        current_directory = os.getcwd()
        print("Directory (root):", current_directory)

        script_info = self.scripts[script_name]
        if os.path.exists(f"{script_name}/{script_name}"):
            script_info["start_button"].config(state=tk.NORMAL)



    def configure_script(self, script_name):
        script_info = self.scripts[script_name]
        config_value = self.config_entry.get()
        if config_value:
            print(f"Configuration value for {script_name}: {config_value}")
            script_info["config_entry_value"] = config_value
            script_info["config_label"].config(text=f"Configuration for {script_info['display_name']}: {config_value}")

    def draw_dot(self, canvas, color):
        canvas.delete("all")
        canvas.create_oval(5, 5, 15, 15, fill=color)

    def start_script(self, script_name):
        script_info = self.scripts[script_name]
        port_number = urlparse(script_info["url"]).port

        if not script_info["is_running"]:
            script_info["is_running"] = True
            script_info["process"] = subprocess.Popen([script_info["command"]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            script_info["pid"] = script_info["process"].pid

            script_info["status_dot"].config(state=tk.NORMAL)
            self.draw_dot(script_info["status_dot"], "green")
            script_info["stop_button"].config(state=tk.NORMAL)
            script_info["start_button"].config(state=tk.DISABLED)

            link_label_text = f"Open: {port_number}"

            script_info["link_label"].config(text=link_label_text)

            self.save_process_info()

    def stop_script(self, script_name):
        script_info = self.scripts[script_name]
        port_number = urlparse(script_info["url"]).port
        if script_info["is_running"]:
            script_info["is_running"] = False
            script_info["config_entry_value"] = ""
            if script_info["pid"]:
                try:
                    os.kill(script_info["pid"], signal.SIGTERM)
                except OSError:
                    pass

            script_info["status_dot"].config(state=tk.DISABLED)
            self.draw_dot(script_info["status_dot"], "red")
            script_info["stop_button"].config(state=tk.DISABLED)
            script_info["start_button"].config(state=tk.NORMAL)

            link_label_text = f"Closed: {port_number}"
            script_info["link_label"].config(text=link_label_text)

            self.save_process_info()

    def open_browser(self, event, url):
        webbrowser.open(url)

    def check_existing_processes(self):
        try:
            with open("process_info.json", "r") as file:
                saved_info = json.load(file)

            for script_name, script_info in saved_info.items():
                if script_name in self.scripts:
                    self.scripts[script_name]["is_running"] = script_info["is_running"]
                    self.scripts[script_name]["pid"] = script_info["pid"]
        except FileNotFoundError:
            pass

    def save_process_info(self):
        process_info = {script_name: {"is_running": script_info["is_running"], "pid": script_info["pid"]} for script_name, script_info in self.scripts.items()}
        with open("process_info.json", "w") as file:
            json.dump(process_info, file)


if __name__ == "__main__":

    app = PulseChainLive()

