import tkinter as tk
import threading
import time
import keyboard
import pyperclip

from jp_overlay.popup import PopupWindow
from jp_overlay.services import get_furigana, translate_ja_to_en
from jp_overlay.config import load_settings, save_settings, set_autostart
from jp_overlay.tray import TrayIcon


def build_theme(dark_mode: bool):
    if dark_mode:
        return {
            "bg": "#202124",
            "fg": "#e8eaed",
            "text_bg": "#303134",
            "text_fg": "#e8eaed",
        }
    else:
        return {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "text_bg": "#ffffff",
            "text_fg": "#000000",
        }


class JPOverlayApp:
    def __init__(self):
        self.settings = load_settings()
        set_autostart(self.settings.get("autostart", True))

        self.root = tk.Tk()
        self.root.withdraw()
        self.theme = build_theme(self.settings.get("dark_mode", True))
        self.popup = None

        # FIX 2 — stable hotkey registration
        hotkey = self.settings.get("hotkey", "ctrl+alt+shift+q")
        keyboard.add_hotkey(hotkey, self.on_hotkey, suppress=True)

        self.tray = TrayIcon(self.exit_app)
        self.tray.start()

    def on_hotkey(self):
        # FIX 1 — prevent multiple popups
        if self.popup is not None:
            try:
                self.popup.destroy()
            except:
                pass
            self.popup = None

        threading.Thread(target=self.process_hotkey, daemon=True).start()

    def process_hotkey(self):
        keyboard.send("ctrl+c")
        time.sleep(0.15)

        text = pyperclip.paste().strip()
        if not text:
            return

        self.show_loader()

        def worker():
            reading = get_furigana(text)
            translation = translate_ja_to_en(text)
            self.update_popup(text, reading, translation)

        threading.Thread(target=worker, daemon=True).start()

    def show_loader(self):
        self.popup = PopupWindow(self.root, self.theme, "Loading...", "", "")
        self.popup.show_near_cursor()

    def update_popup(self, original, reading, translation):
        if self.popup:
            self.popup.update_content(original, reading, translation)

    def exit_app(self):
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass
        self.root.quit()

    def run(self):
        self.root.mainloop()


def main():
    app = JPOverlayApp()
    app.run()


if __name__ == "__main__":
    main()