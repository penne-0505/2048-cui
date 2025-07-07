# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# プロジェクトのルートディレクトリ
root_dir = Path(__file__).parent

# アプリケーションのメイン設定
a = Analysis(
    ['src/main.py'],
    pathex=[str(root_dir)],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('src/config.json', 'src'),
    ],
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

# アプリケーションのPYZ設定
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 実行可能ファイルの設定
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='2048-cli',
    debug=False,
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
    icon=None,
)

