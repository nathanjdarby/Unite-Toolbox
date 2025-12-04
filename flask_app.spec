# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Unite Toolbox Flask Web Application

block_cipher = None

a = Analysis(
    ['archive/flask_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('archive/templates', 'templates'),  # Include all template files
        ('config.py', '.'),                  # Include config
        ('utils.py', '.'),                   # Include utils
        ('gui_components.py', '.'),         # Include GUI components (if needed)
    ],
    hiddenimports=[
        'flask',
        'pandas',
        'premailer',
        'werkzeug',
        'jinja2',
        'zipfile',
        'io',
        'os',
        're',
        'subprocess',
        'webbrowser',
        'pyperclip',
        'requests',
        'beautifulsoup4',
        'bs4',
        'openpyxl',
        'json',
        'threading',
        'time',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # Don't exclude - let PyInstaller handle dependencies
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
    name='UniteToolboxWeb',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console to show Flask output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,  # Build for current architecture (arm64 works on Intel via Rosetta 2)
    codesign_identity=None,
    entitlements_file=None,
)

# For macOS, create an app bundle
app = BUNDLE(
    exe,
    name='UniteToolboxWeb.app',
    icon=None,  # You can add an icon file here if you have one
    bundle_identifier='org.unitetheunion.toolbox.web',
    info_plist={
        'CFBundleName': 'Unite Toolbox Web',
        'CFBundleDisplayName': 'Unite Toolbox Web',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSBackgroundOnly': False,  # Show in dock
    },
)

