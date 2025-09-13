from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path


def find_bytes(exe_path: Path, to_find: bytes) -> int | None:
    """Find the position of the bytes in the executable file."""
    prev = b""
    with exe_path.open("rb") as f:
        while True:
            concat_pos = 0
            buf = f.read(max(2048**2, 9))
            if not buf:
                break
            concat = prev + buf
            while True:
                concat_pos = concat.find(to_find, concat_pos)
                if concat_pos == -1:
                    break
                return f.tell() + concat_pos - len(concat)
            prev = buf[-9 + 1 :]


def write_bytes(exe_path: Path, pos: int, to_write: bytes) -> None:
    """Write the bytes to the executable file."""
    with exe_path.open("rb+") as f:
        f.seek(pos)
        f.write(to_write)


def find_steam_cp77() -> Path | None:
    """Find Cyberpunk 2077 in the default Steam directory."""
    steam_path = Path("C:/Program Files (x86)/Steam/steamapps/common/Cyberpunk 2077")
    if steam_path.exists():
        exe_path = steam_path / "bin" / "x64" / "Cyberpunk2077.exe"
        if exe_path.exists():
            return exe_path
    return None


def find_exe_path(path: Path) -> Path:
    """Find the executable file in the given path."""
    # Determine the exe path
    if path.is_file() and path.name == "Cyberpunk2077.exe":
        # Direct path to exe file
        exe_path = path
    elif path.is_dir():
        # Directory path, look for exe in bin/x64 subdirectory
        exe_path = path / "bin" / "x64" / "Cyberpunk2077.exe"
    else:
        # Assume it's a directory and try to find exe
        exe_path = path / "Cyberpunk2077.exe"

    # Verify the exe file exists
    if not exe_path.exists():
        print(f"Error: Could not find Cyberpunk2077.exe at {exe_path}")
        print("Usage: python main.py [--unpatch] [path]")
        sys.exit(1)

    return exe_path


def check_paths(args: argparse.Namespace) -> Path:
    """Check the paths and return the executable path."""
    if not args.path:
        steam_exe = find_steam_cp77()
        if steam_exe:
            print(f"Found Cyberpunk 2077 at: {steam_exe}")
            confirm = input("Use this executable? (y/n): ").lower().strip()
            if confirm in {"y", "yes"}:
                exe_path = steam_exe
            else:
                print("Please rerun the script and specify the path manually.")
                sys.exit(0)
        else:
            print("Could not find Cyberpunk 2077 in Steam directory.")
            print("Please rerun the script and specify the path manually.")
            sys.exit(0)
    else:
        exe_path = find_exe_path(args.path)

    return exe_path


def patch_exe(exe_path: Path, unpatch: bool = False) -> None:
    """Patch or unpatch the executable file.

    Raises:
        Exception: If the bytes are not found.
    """
    if unpatch:
        action = "Unpatching"
        to_find = b"\xff\x90\x70\x01\x00\x00\x83\x7c\x24\x20\x00\x90\x90"
        to_write = b"\xff\x90\x70\x01\x00\x00\x83\x7c\x24\x20\x00\x75\x10"
    else:
        action = "Patching"
        to_find = b"\xff\x90\x70\x01\x00\x00\x83\x7c\x24\x20\x00\x75\x10"
        to_write = b"\xff\x90\x70\x01\x00\x00\x83\x7c\x24\x20\x00\x90\x90"

    print(f"{action}: {exe_path}")

    print(f"{action} binary...")
    pos = find_bytes(exe_path, to_find)
    if not pos:
        msg = f"Couldn't find bytes. Already {'unpatched' if action == 'Patching' else 'patched'}?"
        raise Exception(msg)
    write_bytes(exe_path, pos, to_write)
    print(f"{action} complete.")


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description="Patch Cyberpunk 2077 to allow saving at any time")
    parser.add_argument(
        "--unpatch",
        action="store_true",
        help="unpatch the game (restore original save restrictions)",
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        help="path to Cyberpunk 2077 directory or executable",
    )
    return parser.parse_args()


def main() -> None:
    """Main function."""
    args = parse_args()
    exe_path = find_exe_path(args.path)

    try:
        patch_exe(exe_path, args.unpatch)
    except KeyboardInterrupt:
        pass
    except Exception:
        traceback.print_exc()
    finally:
        input("Press Enter to exit.")


if __name__ == "__main__":
    main()
