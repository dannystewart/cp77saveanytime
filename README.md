# Cyberpunk 2077 Save Anytime (v2.3)

A simple utility to patch `Cyberpunk2077.exe` to allow saving when it would normally be blocked. Based on [Save Anytime](https://www.nexusmods.com/cyberpunk2077/mods/610) by Sorrow446, updated for Cyberpunk 2077 v2.3.

## Usage

Clone the repo, then run using one of the methods below.

Using Poetry:

```bash
poetry install
poetry run cp77saver "C:\Program Files (x86)\Steam\steamapps\common\Cyberpunk 2077"
```

Using pip:

```bash
pip install .
cp77saver "C:\Program Files (x86)\Steam\steamapps\common\Cyberpunk 2077"
```

Without installing:

```bash
python cp77saver.py "C:\Program Files (x86)\Steam\steamapps\common\Cyberpunk 2077"
```

If no argument is given, it'll try to find it in the default Steam directory. It can also be run directly from the game's root folder or the `bin\x64` subfolder and it'll find the EXE automatically.
