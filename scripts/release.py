"""Build a portable package ZIP without local servers or machine-specific paths."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parent.parent
output = root / 'dist' / 'bbedit-nickel-0.1.0.zip'
output.parent.mkdir(exist_ok=True)
with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
    for path in sorted((root / 'Nickel.bbpackage').rglob('*')):
        if path.is_file():
            archive.write(path, path.relative_to(root))
    for name in ('README.md', 'LICENSE', 'CHANGELOG.md'):
        archive.write(root / name, name)
    archive.write(root / 'examples/highlighting.ncl', 'examples/highlighting.ncl')
print(output)
