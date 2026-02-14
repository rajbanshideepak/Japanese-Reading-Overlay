JPOverlay — Instant Japanese Reading & Translation Popup Tool
=============================================================

JPOverlay is a lightweight Windows utility that instantly shows hiragana
reading and English translation for any selected Japanese text.
Select text → press your hotkey → a popup appears near your cursor.

This tool is designed for learners, developers, and anyone working with
Japanese text who wants fast, distraction‑free reading support.


---------------------------------------------------------------
FEATURES
---------------------------------------------------------------

• Instant Popup  
  Select Japanese text anywhere and press your hotkey.
  Default hotkey: Ctrl + Alt + Shift + Q

• Hiragana Reading (with spacing)
  - Kanji → reading via Janome tokenizer
  - Katakana → converted to Hiragana
  - Natural spacing between words

• English Translation
  - Uses MyMemory API (free, stable, no API key required)
  - Works with long text

• Clean Dark Mode UI
  - Selectable text
  - Resizable window
  - Smooth drag behavior
  - Popup closes only when clicking outside

• System Tray Icon
  - Dark square with “JP”
  - Right‑click → Exit

• Auto‑Start with Windows
  The build script automatically places the EXE into the Startup folder.

• Clean Build Output
  - Final EXE stored in Release/
  - build/ and dist/ folders removed automatically
  - Startup EXE updated automatically


---------------------------------------------------------------
PROJECT STRUCTURE
---------------------------------------------------------------

Kanji Reading Tool/
  jp_overlay/
    __init__.py
    main.py
    popup.py
    services.py
    config.py
    tray.py
  settings.json
  requirements.txt
  jp_overlay.spec
  setup_env.bat
  build_exe.bat
  README.txt


---------------------------------------------------------------
SETTINGS (settings.json)
---------------------------------------------------------------

{
  "hotkey": "ctrl+alt+shift+q",
  "autostart": true,
  "dark_mode": true
}

You can edit:
- hotkey
- autostart
- dark_mode


---------------------------------------------------------------
INSTALLATION
---------------------------------------------------------------

1. Clone the repository:
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>

2. Create virtual environment & install dependencies:
   setup_env.bat


---------------------------------------------------------------
RUNNING IN DEVELOPMENT MODE
---------------------------------------------------------------

call .venv\Scripts\activate
python -m jp_overlay.main


---------------------------------------------------------------
BUILDING THE EXE
---------------------------------------------------------------

Run:
  build_exe.bat

This script will:
  1. Build the EXE using PyInstaller
  2. Copy the EXE into Release/
  3. Delete build/ and dist/
  4. Remove any old EXE from Windows Startup
  5. Copy the new EXE into the Startup folder

Final EXE:
  Release/JPOverlay.exe


---------------------------------------------------------------
HOW TO USE
---------------------------------------------------------------

1. Select Japanese text anywhere
2. Press your hotkey
3. Popup appears near your cursor showing:
   - Original text
   - Hiragana reading
   - English translation
4. Resize the popup from the bottom‑right corner
5. Click outside the popup to close it
6. Right‑click tray icon → Exit

---------------------------------------------------------------
REQUIREMENTS
---------------------------------------------------------------

• Windows 10 or Windows 11
• Python 3.10+ (for development)
• Internet required for translation
• No internet required for reading


