import threading
from PIL import Image, ImageDraw, ImageFont
import pystray


class TrayIcon:
    def __init__(self, on_exit_callback):
        self.on_exit_callback = on_exit_callback
        self.icon = pystray.Icon("JPOverlay", self._create_image(), "JP Overlay", self._menu())
        self.thread = threading.Thread(target=self.icon.run, daemon=True)

    def _create_image(self):
        # Create a 64x64 dark square
        img = Image.new("RGBA", (64, 64), "#202124")  # dark gray background
        draw = ImageDraw.Draw(img)

        # Draw border
        draw.rectangle((0, 0, 63, 63), outline="#FFFFFF", width=3)

        # Load default font
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()

        # Center "JP"
        text = "JP"
        text_w, text_h = draw.textsize(text, font=font)
        x = (64 - text_w) // 2
        y = (64 - text_h) // 2 - 2

        draw.text((x, y), text, fill="#FFFFFF", font=font)

        return img

    def _menu(self):
        return pystray.Menu(
            pystray.MenuItem("Exit", self._on_exit)
        )

    def _on_exit(self, icon, item):
        self.icon.stop()
        if self.on_exit_callback:
            self.on_exit_callback()

    def start(self):
        self.thread.start()