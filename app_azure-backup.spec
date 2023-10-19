# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app_azure.py'],
    pathex=[],
    binaries=[],
    datas=[('01-processing-files/*', '01-processing-files'), ('01-processing-files/01-split-sys-msg-method/*', '01-processing-files/01-split-sys-msg-method'), ('01-processing-files/02-simple-method/*', '01-processing-files/02-simple-method')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('v', None, 'OPTION')],
    name='app_azure',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	onefile=True,  # This is the line you add for onefile
)
