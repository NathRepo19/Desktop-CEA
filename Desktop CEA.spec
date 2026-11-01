# Build with: python -m PyInstaller --noconfirm "Desktop CEA.spec"
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
from PyInstaller.utils.hooks.qt import pyside6_library_info

root = Path(SPECPATH)
# A mixed Anaconda/PyPI installation can report Anaconda's Qt plugin paths.
# Keep plugins and DLLs from the same PySide6 wheel whenever it bundles Qt.
qt_package = pyside6_library_info.package_location
if (qt_package / "Qt6Core.dll").is_file():
    pyside6_library_info.qt_inside_package = True
    pyside6_library_info.qt_lib_dir = qt_package
    for key, relative in {
        "PrefixPath": ".", "BinariesPath": ".", "LibrariesPath": ".",
        "PluginsPath": "plugins", "TranslationsPath": "translations",
        "QmlImportsPath": "qml", "DataPath": ".",
    }.items():
        pyside6_library_info.location[key] = str(qt_package / relative)

rocketcea_data = collect_data_files(
    "rocketcea", include_py_files=True,
    includes=["*.inp", "*.lib", "_version.py", "*LICENSE*"],
)

a = Analysis(
    [str(root / "main.py")],
    pathex=[str(root)],
    binaries=collect_dynamic_libs("rocketcea"),
    datas=rocketcea_data + [(str(root / "icon.png"), ".")],
    hiddenimports=["rocketcea.py_cea"],
    hookspath=[],
    hooksconfig={"matplotlib": {"backends": ["QtAgg"]}},
    runtime_hooks=[],
    excludes=["PyQt5", "PyQt6", "PySide2", "IPython", "pytest", "tkinter"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="Desktop CEA",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(root / "icon.ico"),
)
