"""List Blender scene objects read-only through the bundled SDNA reader."""
import argparse, json
from pathlib import Path
from readblend import Blend

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('blend', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    scene = Blend(args.blend)
    objects = []
    for ob in scene.bytype.get('Object', []):
        objects.append({'name': scene.get(ob, 'id.name')[2:],
                        'object_addr': ob['addr'],
                        'data_addr': scene.get(ob, 'data'),
                        'type': scene.get(ob, 'type')})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(objects, ensure_ascii=False, indent=2))
    print(f'Cataloged {len(objects)} objects; geometry must be checked before selection.')

if __name__ == '__main__':
    main()
