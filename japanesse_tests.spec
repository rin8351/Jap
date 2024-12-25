# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (r'C:\Users\Rin\tutorial\Jap\japanese_background.png', '.'),
        (r'C:\Users\Rin\tutorial\Jap\japanese_background2.png', '.'),
        (r'C:\Users\Rin\tutorial\Jap\japanese_logo.png', '.'),
        (r'C:\Users\Rin\tutorial\Jap\main.ico', '.'),
    ],
    hiddenimports=['pandas','openpyxl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='japanesse_tests',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['main.ico'],
)
