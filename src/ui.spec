# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['ui.pyw'],
             pathex=['C:\\Users\\danie\\Desktop\\git\\Chess\\src'],
             binaries=[],
             datas=[('C:\\Users\\danie\\Desktop\\git\\Chess\\src\\Textures\\*.png', 'Textures')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
