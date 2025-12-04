# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Unite Toolbox (Refactored App)

block_cipher = None

a = Analysis(
    ['app_refactored.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.py', '.'),          # Include config
        ('utils.py', '.'),           # Include utils
        ('gui_components.py', '.'),  # Include GUI components
        ('validate-jot.py', '.'),    # Include validator script
    ],
    hiddenimports=[
        'pandas',
        'premailer',
        'pyperclip',
        'openpyxl',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        'webbrowser',
        'requests',
        'beautifulsoup4',
        'bs4',
        'tkhtmlview',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='UniteToolbox',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,  # Build for current architecture (universal2 requires all deps to be universal)
    codesign_identity=None,
    entitlements_file=None,
)

# For macOS, create an app bundle
app = BUNDLE(
    exe,
    name='UniteToolbox.app',
    icon=None,  # You can add an icon file here if you have one
    bundle_identifier='org.unitetheunion.toolbox',
    info_plist={
        'CFBundleName': 'Unite Toolbox',
        'CFBundleDisplayName': 'Unite Toolbox',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
    },
)

