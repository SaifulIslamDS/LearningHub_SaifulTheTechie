#!/usr/bin/env python3
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1]
FIXED=(2026,1,1,0,0,0)

def zip_tree(src:Path,dest:Path,prefix:str):
    dest.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(x for x in src.rglob('*') if x.is_file()):
            zi=zipfile.ZipInfo(f'{prefix}/{f.relative_to(src).as_posix()}',date_time=FIXED)
            zi.compress_type=zipfile.ZIP_DEFLATED; zi.external_attr=0o644<<16
            z.writestr(zi,f.read_bytes())
    print(dest.relative_to(ROOT))

zip_tree(ROOT/'examples/level-01/javascript',ROOT/'content/downloads/level-01/javascript-foundations.zip','javascript-foundations')
zip_tree(ROOT/'examples/level-01/web-foundations',ROOT/'content/downloads/level-01/web-foundations-starter.zip','web-foundations')
zip_tree(ROOT/'examples/level-01/react-starter',ROOT/'content/downloads/level-01/react-vite-starter-reference.zip','react-vite-starter-reference')
zip_tree(ROOT/'examples/level-01/nextjs-fullstack-reference',ROOT/'content/downloads/level-01/nextjs-fullstack-reference.zip','nextjs-fullstack-reference')
zip_tree(ROOT/'examples/level-01/backend-mongodb-practice',ROOT/'content/downloads/level-01/backend-mongodb-practice.zip','backend-mongodb-practice')
zip_tree(ROOT/'examples/level-01/fullstack-project-1',ROOT/'content/downloads/level-01/fullstack-project-1-blueprint.zip','fullstack-project-1-blueprint')

# Combined TypeScript + framework-independent React logic.
dest=ROOT/'content/downloads/level-01/typescript-react-foundations.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
    for src in [ROOT/'examples/level-01/typescript',ROOT/'examples/level-01/react-logic']:
        for f in sorted(x for x in src.rglob('*') if x.is_file()):
            zi=zipfile.ZipInfo(f'typescript-react-foundations/{src.name}/{f.relative_to(src).as_posix()}',date_time=FIXED)
            zi.compress_type=zipfile.ZIP_DEFLATED; zi.external_attr=0o644<<16; z.writestr(zi,f.read_bytes())
print(dest.relative_to(ROOT))
