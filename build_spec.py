# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Nonprofit Idea Coach
This creates a standalone executable with all dependencies bundled
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all data files
datas = [
    ('nonprofit_coach/templates', 'templates'),
    ('nonprofit_coach/static', 'static'),
    ('nonprofit_coach/.env.example', '.'),
    ('nonprofit_coach/README.md', '.'),
]

# Collect all hidden imports
hiddenimports = [
    'anthropic',
    'flask',
    'dotenv',
    'sqlite3',
    'gunicorn',
]

# Add search provider modules
hiddenimports.extend(collect_submodules('nonprofit_coach.search_providers'))

a = Analysis(
    ['nonprofit_coach/app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='NonprofitIdeaCoach',
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
