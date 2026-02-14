import tkinter as tk
from tkinter import ttk
import pyautogui
import time


class PopupWindow(tk.Toplevel):
    def __init__(self, master, theme, original="", reading="", translation=""):
        super().__init__(master)

        self.theme = theme
        self.title("JP Overlay")
        self.attributes("-topmost", True)
        self.geometry("460x420")

        self.resizable(True, True)

        self.has_focus = False
        self.created_time = time.time()

        bg = theme["bg"]
        fg = theme["fg"]
        self.configure(bg=bg)

        # --- UI ---
        self.text_original = self._make_section("Original:", original, bg, fg)
        self.text_reading = self._make_section("Reading (ひらがな):", reading, bg, fg)
        self.text_translation = self._make_section("Translation:", translation, bg, fg)

        # Resize grip
        grip = ttk.Sizegrip(self)
        grip.pack(side="right", anchor="se")

        # Dragging only when clicking on background (NOT text)
        self.bind("<Button-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)

        # Focus tracking
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        # Timer for "never focused" auto-close
        self.after(500, self.check_initial_focus)

    def _make_section(self, label, content, bg, fg):
        lbl = tk.Label(self, text=label, font=("Segoe UI", 10, "bold"), bg=bg, fg=fg)
        lbl.pack(anchor="w", padx=5)

        txt = tk.Text(
            self,
            height=3,
            wrap="word",
            bg=self.theme["text_bg"],
            fg=self.theme["text_fg"],
            insertbackground=self.theme["text_fg"]
        )
        txt.insert("1.0", content)
        txt.config(state="normal")  # allow selection
        txt.pack(fill="both", expand=True, padx=5, pady=3)

        # Prevent dragging when clicking inside text
        txt.bind("<Button-1>", lambda e: None)

        return txt

    # --- Dragging ---
    def start_move(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)

        # If clicking inside Text widget → do NOT drag
        if isinstance(widget, tk.Text):
            self.dragging = False
            return

        # If clicking on resize grip → do NOT drag
        if isinstance(widget, ttk.Sizegrip):
            self.dragging = False
            return

        # Enable dragging
        self.dragging = True
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root

        # Current window position
        self.win_start_x = self.winfo_x()
        self.win_start_y = self.winfo_y()

    def do_move(self, event):
        # If not dragging → ignore
        if not getattr(self, "dragging", False):
            return

        # Calculate movement
        dx = event.x_root - self.drag_start_x
        dy = event.y_root - self.drag_start_y

        # Move window
        new_x = self.win_start_x + dx
        new_y = self.win_start_y + dy
        self.geometry(f"+{new_x}+{new_y}")

    # --- Focus handling ---
    def on_focus_in(self, event):
        self.has_focus = True

    def on_focus_out(self, event):
        # Close only if it was focused before
        if self.has_focus:
            self.destroy()

    # --- Auto-close if never focused ---
    def check_initial_focus(self):
        if not self.has_focus:
            if time.time() - self.created_time > 5:
                self.destroy()
                return
        self.after(500, self.check_initial_focus)

    # --- Show near cursor ---
    def show_near_cursor(self):
        x, y = pyautogui.position()
        self.geometry(f"+{x+10}+{y+10}")
        self.deiconify()
        self.lift()
        self.focus_force()

    # --- Update content ---
    def update_content(self, original, reading, translation):
        self._update_text(self.text_original, original)
        self._update_text(self.text_reading, reading)
        self._update_text(self.text_translation, translation)

    def _update_text(self, widget, content):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", content)
        widget.config(state="normal")