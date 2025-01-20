import Tkinter as tk
import threading
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Responsive Tkinter Example")

        # Set up the UI components
        self.label = tk.Label(root, text="Starting...")
        self.label.pack(pady=20)

        self.button = tk.Button(root, text="Start Background Work", command=self.start_background_task)
        self.button.pack(pady=10)
        self.root.after(100, self.update_gui)  # Call the update_gui method every 100ms
        self.is_working = False  # To track if the background task is running

    def start_background_task(self):
        if not self.is_working:
            self.is_working = True
            self.label.config(text="Working in background...")
            # Start the background thread
            threading.Thread(target=self.background_task).start()

    def background_task(self):
        # Simulate some background work with a loop
        for i in range(10):
            if not self.is_working:
                break
            time.sleep(1)  # Simulate long task
            print("Background task iteration %d completed." % (i + 1))
        
        # Once the task is done, update the UI
        self.is_working = False
        self.root.after(0, self.update_gui)  # Call GUI update on the main thread

    def update_gui(self):
        # Update the GUI without blocking
        if self.is_working:
            self.label.config(text="Working in background...")
        else:
            self.label.config(text="Background task finished!")

        # Schedule the update_gui method again in 100ms
        self.root.after(100, self.update_gui)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
