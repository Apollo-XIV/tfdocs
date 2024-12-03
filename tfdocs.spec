# -*- mode: python ; coding: utf-8 -*-
import os

# base_dir = os.path.abspath(os.path.dirname(__file__))
musl_path = os.environ.get('MUSL_PATH')
zlib_path = os.environ.get('ZLIB_PATH')

binary_paths = [
    (p, ".")
    for p in
    [
        musl_path,
        zlib_path
    ]
]
# print(binary_paths)

a = Analysis(
    [os.path.join('tfdocs', '__main__.py')],
    pathex=[],
    binaries=binary_paths,
    datas=[],
    hiddenimports=[
        "textual.widgets._markdown_viewer",
        "textual.widgets._tab_pane",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='tfdocs',
    exclude_binaries=False,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
