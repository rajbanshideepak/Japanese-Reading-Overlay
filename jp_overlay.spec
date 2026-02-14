# jp_overlay.spec

block_cipher = None

import os
import site

# Try to locate janome sysdic automatically
site_dirs = site.getsitepackages()
janome_sysdic = None
for d in site_dirs:
    candidate = os.path.join(d, "janome", "sysdic")
    if os.path.isdir(candidate):
        janome_sysdic = candidate
        break

datas = []
if janome_sysdic:
    datas.append((janome_sysdic, "janome/sysdic"))

a = Analysis(
    ['jp_overlay/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['janome', 'janome.sysdic'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='JPOverlay',
    debug=False,
    strip=False,
    upx=False,
    console=False
)