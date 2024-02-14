# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

excluded_binaries = [
    "PySide6\\Qt6OpenGL.dll",
    "PySide6\\Qt6Pdf.dll",
    "PySide6\\Qt6Qml.dll",
    "PySide6\\Qt6QmlModels.dll",
    "PySide6\\Qt6Network.dll",
    "PySide6\\Qt6Quick.dll",
    "PySide6\\Qt6VirtualKeyboard.dll",
    "PySide6\\Qt6Svg.dll",
    "PySide6\\MSVCP140_1.dll",
    "PySide6\\MSVCP140_2.dll",
    "PySide6\\opengl32sw.dll",
    "PySide6\\VCRUNTIME140_1.dll",
    "PySide6\\MSVCP140.dll",

    'VCRUNTIME140.dll',
    'msvcp140.dll',
    'mfc140u.dll',
    'libcrypto-1_1.dll',
    'libssl-1_1.dll',
    # 'unicodedata.pyd',  # NOTE: DO NOT  UNCOMMENT required by a7p library
    'shiboken6\\MSVCP140.dll',
    'shiboken6\\VCRUNTIME140_1.dll',
]


a.binaries = TOC([x for x in a.binaries if x[0] not in excluded_binaries])

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='mbc2drg',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
