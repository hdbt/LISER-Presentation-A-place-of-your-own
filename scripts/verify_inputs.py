import hashlib, json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for name,expected in json.loads((root/'INPUT_SHA256.json').read_text()).items():
    actual=hashlib.sha256((root/name).read_bytes()).hexdigest()
    if actual!=expected: raise ValueError('Input checksum mismatch: '+name)
print('PASS: input snapshot and dependency checksums')
