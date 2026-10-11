"""Run on desktop CPython: python tests/static_checks.py"""
from pathlib import Path
import ast
base=Path(__file__).resolve().parents[1]
for path in base.rglob('*.py'):
    ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
assert (base/'lib/display.py').is_file()
assert (base/'lib/sdcard.py').is_file()
print('Static checks passed')
