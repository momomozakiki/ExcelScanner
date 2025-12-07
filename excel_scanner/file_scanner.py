import json
from typing import Union
from pathlib import Path

class FileScanner:
    def __init__(self, filepath: Union[str, Path], config_path: Union[str, Path] = None):
        self.filepath = Path(filepath)
        print('file path : ', self.filepath)

        # Resolve config path
        if config_path is None:
            print('before config_path : ', config_path)
            config_path = Path(__file__).parent / "config" / "quotation_scanner_setting.json"
            print('config_path : ', config_path)
        else:
            print('config_path found: ', config_path)
            config_path = Path(config_path)

        # --- Safety checks with clear diagnostics ---
        print(f"[INFO] Loading config from: {config_path.resolve()}")

        if not config_path.exists():
            raise FileNotFoundError(
                f"❌ Config file not found.\n"
                f"👉 Please create: {config_path}\n"
                f"💡 You can use the example from earlier conversation."
            )

        try:
            with open(config_path, encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Invalid JSON in config file: {e}") from e

        # Assign sections — use .get() with defaults to avoid KeyError if schema evolves
        self.page_header = config.get("page_header", {})
        self.cell_offset_info = config.get("cell_offset_info", {})
        self.content = config.get("content", {})

        # Validate required top-level keys
        required = ["page_header", "cell_offset_info", "content"]
        missing = [k for k in required if k not in config]
        if missing:
            raise KeyError(f"❌ Missing required sections in config: {missing}")

        print("[INFO] Config loaded successfully.")


# ───────────────────────────────────────────────────────
# 🧪 Test block: only checks + loads real config — no duplication
# ───────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🧪 Running self-test for FileScanner...")
    file_path = Path(__file__).parent / "config" / "quotation_scanner_setting.json"

    try:
        # Try to instantiate with a dummy file
        # scanner = FileScanner("dummy_quote.xlsx")
        scanner = FileScanner(file_path)
        print('scanner: ', scanner.content)
        print(scanner.page_header)

        print("\n✅ Config summary:")
        print(f"  • Page header fields: {len(scanner.page_header)}")
        print(f"  • Offset rules: {list(scanner.cell_offset_info.keys())}")
        print(f"  • Content keywords: {scanner.content.get('keyword', [])}")

    except Exception as e:
        print(f"\n💥 Test failed: {e}")
        import sys
        sys.exit(1)
    else:
        print("\n🎉 Self-test passed.")