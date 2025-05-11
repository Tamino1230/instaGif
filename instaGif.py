import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askinteger
from pynput import keyboard
import pyautogui
import os
import time
import threading
from rich import print


class Gif:
    def __init__(self):
        self.root = None
        self.x_entry = None
        self.y_entry = None
        self.width_entry = None
        self.height_entry = None

        self.hotkey = keyboard.Key.f2;
        self.transparency = 0.8

    def print_info(self):
        print("[bold magenta]Thank you for Downloading instaGif![/bold magenta]\n[bold blue]by https://github.com/Tamino1230[/bold blue]\n")
        print("[bold yellow]Press F2 to open the GUI.[/bold yellow]")
        print("[bold yellow]Move the window to select the area you want to capture.[/bold yellow]")
        print("[bold yellow]Press 'Start' to begin capturing GIF.[/bold yellow]")
        print("[bold yellow]Press 'Open Output Folder' to view saved GIFs.[/bold yellow]")
        print("[bold yellow]Press 'Update Coordinates' to refresh the coordinates (If it refreshes wrong).[/bold yellow]")
    

    def open_output_folder(self):
        output_folder = os.path.join(os.getcwd(), "gif_outputs")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        os.startfile(output_folder)


    def create_gui(self):
        print("[bold green]Creating GUI...[/bold green]")
        self.root = tk.Tk()
        self.root.title("Move Window to Select Area ~ Tamino1230")

        #- window transparency
        self.root.wm_attributes("-topmost", True)
        self.root.attributes("-alpha", self.transparency)
        self.root.geometry("300x200")
        self.root.wm_attributes("-toolwindow", True)

        tk.Label(self.root, text="X-Position").grid(row=0)
        self.x_entry = tk.Entry(self.root)
        self.x_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Y-Position").grid(row=1)
        self.y_entry = tk.Entry(self.root)
        self.y_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Width").grid(row=2)
        self.width_entry = tk.Entry(self.root)
        self.width_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Height").grid(row=3)
        self.height_entry = tk.Entry(self.root)
        self.height_entry.grid(row=3, column=1)

        open_folder_button = tk.Button(self.root, text="Open Output Folder", command=self.open_output_folder)
        open_folder_button.grid(row=5, columnspan=2)

        update_button = tk.Button(self.root, text="Update Coordinates", command=self.update_coordinates)
        update_button.grid(row=4, columnspan=2)

        start_button = tk.Button(self.root, text="Start", command=self.start_capture)
        start_button.grid(row=6, columnspan=2)

        #- update on window move
        self.root.bind("<Configure>", lambda event: self.update_coordinates())

        self.root.mainloop()
        print("[bold red]GUI closed.[/bold red]")


    def update_coordinates(self):
        self.root.update_idletasks()
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        self.x_entry.delete(0, tk.END)
        self.y_entry.delete(0, tk.END)
        self.width_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.x_entry.insert(0, x)
        self.y_entry.insert(0, y)
        self.width_entry.insert(0, w)
        self.height_entry.insert(0, h)


    def get_coordinates(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            w = int(self.width_entry.get())
            h = int(self.height_entry.get())
            return x, y, w, h
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid int values.")
            return None


    def start_capture(self):
        coordinates = self.get_coordinates()
        if coordinates and all(coordinates):
            duration = askinteger("GIF Duration", "Enter the duration of the GIF in seconds:", minvalue=1, maxvalue=60, parent=self.root)
            self.root.wm_attributes("-topmost", True)
            self.root.wm_attributes("-toolwindow", True)
            if duration is None or duration <= 0:
                messagebox.showerror("Input Error", "Please enter a valid duration.")
                return

            x, y, w, h = coordinates
            region = (x, y, w, h)

            self.root.withdraw()

            threading.Thread(target=self.capture_gif, args=(region, duration), daemon=True).start()
        else:
            messagebox.showerror("Input Error", "Please fill in all fields with valid values.")


    def capture_gif(self, region, duration):
        frames = []
        start_time = time.time()
        first = True

        print("[yellow]Capturing frames...[/yellow]")
        while time.time() - start_time < duration:
            if first:
                first = False
                time.sleep(0.5)
            screenshot = pyautogui.screenshot(region=region)
            frames.append(screenshot)
            
            time.sleep(0.1)
            print(f"[bold green]Captured frame {len(frames)}[/bold green]")
        print("[green]Finished capturing frames.[/green]")
        print("[yellow]Creating GIF...[/yellow]")
        if not os.path.exists("gif_outputs"):
            os.makedirs("gif_outputs")
        output_path = os.path.join(os.getcwd(), f"gif_outputs/output_{time.time()}.gif")
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=100, loop=0)
        print(f"GIF saved at {output_path}")
        messagebox.showinfo("Capture Complete", f"GIF saved at {output_path}")

        self.root.deiconify()


    def on_press(self, key):
        try:
            if key == self.hotkey:
                self.create_gui()
        except Exception as e:
            print(f"An error occurred: {e}")


    def start_hotkey_listener(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    


if __name__ == "__main__":
    gif = Gif()
    gif.print_info()
    gif.start_hotkey_listener()