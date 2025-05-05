import pyautogui
import tkinter as tk
from tkinter import ttk
import threading
import time
from PIL import Image, ImageTk  # Import for handling the logo image

class AutoMouseMover:
    def __init__(self, root):
        self.root = root
        self.root.title("Ecolab Automouse™")
        self.root.configure(bg="#f1f1f1")  # Set background to light gray
        self.root.geometry("400x500")  # Adjust window size to add space at the bottom
        self.running = False
        self.create_widgets()

    def create_widgets(self):
        # Add Title
        title_label = tk.Label(
            self.root,
            text="Ecolab Automouse™",
            font=("Helvetica", 16, "bold"),
            bg="#f1f1f1",
            fg="#006bd3"
        )
        title_label.pack(pady=(10, 10))  # Add padding below the title

        # Frame for Duration Label and Combo Box
        duration_frame = tk.Frame(self.root, bg="#f1f1f1")
        duration_frame.pack(pady=5)

        # Duration Label
        duration_label = tk.Label(
            duration_frame,
            text="Duration:",
            font=("Arial", 10, "bold"),
            bg="#f1f1f1",
            fg="#006bd3"
        )
        duration_label.pack(side=tk.LEFT, padx=5)

        # Combo Box for Duration
        self.duration_var = tk.StringVar()
        self.duration_combobox = ttk.Combobox(duration_frame, textvariable=self.duration_var, width=10)
        self.duration_combobox['values'] = ('30 mins', '1 hour', '3 hours', 'Indefinite')
        self.duration_combobox.current(0)
        self.duration_combobox.pack(side=tk.LEFT, padx=5)

        # Frame for Start and Stop Buttons
        button_frame = tk.Frame(self.root, bg="#f1f1f1")
        button_frame.pack(pady=10)

        # Start Button
        self.start_button = ttk.Button(button_frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.start_button.configure(style="Custom.TButton")

        # Stop Button
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.stop_button.configure(style="Custom.TButton")

        # Status Label (moved closer to the canvas)
        self.status_label = ttk.Label(self.root, text="Status: Inactive", foreground="red", background="#f1f1f1")
        self.status_label.pack(pady=(2, 2))  # Reduced padding to move it closer to the canvas

        # Canvas to display the square (replaced with image background)
        canvas_width, canvas_height = 300, 250
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="#f1f1f1", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Load the Ecolab forward pattern image
        pattern_image = Image.open("Ecolab_Forward_Pattern_RGB.jpg")
        pattern_image = pattern_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        self.pattern = ImageTk.PhotoImage(pattern_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.pattern)

        # Add Ecolab logo (moved to bottom middle with padding)
        logo_image = Image.open("ECL_BIG.png")  # Load the logo image
        original_width, original_height = logo_image.size
        new_width = 100  # Set the desired width
        new_height = int((new_width / original_width) * original_height)  # Maintain aspect ratio
        logo_image = logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Resize the image
        self.logo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self.root, image=self.logo, bg="#f1f1f1")
        logo_label.pack(pady=(10, 10))  # Add padding above and below the logo

        # Configure custom button style with bezeling and depth
        style = ttk.Style()
        style.configure(
            "Custom.TButton",
            background="#f1f1f1",
            foreground="#006bd3",
            font=("Arial", 10, "bold"),
            relief="raised",
            borderwidth=3
        )

    def start(self):
        if not self.running:
            self.running = True
            self.update_status("Active", "green")
            self.duration = self.get_duration()
            self.thread = threading.Thread(target=self.move_and_click)
            self.thread.start()

    def stop(self):
        self.running = False
        self.update_status("Inactive", "red")

    def update_status(self, status, color):
        self.status_label.config(text=f"Status: {status}", foreground=color)

    def get_duration(self):
        duration_str = self.duration_var.get()
        if duration_str == '30 mins':
            return 30 * 60
        elif duration_str == '1 hour':
            return 60 * 60
        elif duration_str == '3 hours':
            return 3 * 60 * 60
        else:
            return float('inf')

    def move_and_click(self):
        start_time = time.time()
        while self.running and (time.time() - start_time < self.duration):
            # Move in a square pattern within the canvas
            self.move_mouse(75, 75)
            self.move_mouse(125, 75)
            self.move_mouse(125, 125)
            self.move_mouse(75, 125)

    def move_mouse(self, x, y):
        # Convert canvas coordinates to screen coordinates
        canvas_x = self.canvas.winfo_rootx() + x
        canvas_y = self.canvas.winfo_rooty() + y
        pyautogui.moveTo(canvas_x, canvas_y, duration=0.5)
        pyautogui.click()

        # Replace time.sleep(30) with a loop that checks self.running
        sleep_duration = 30  # Total sleep duration in seconds
        interval = 0.1       # Check interval in seconds
        elapsed = 0
        while elapsed < sleep_duration and self.running:
            time.sleep(interval)
            elapsed += interval

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoMouseMover(root)
    root.mainloop()
