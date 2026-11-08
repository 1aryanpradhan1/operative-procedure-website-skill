# Pterional craniotomy guide

This static project contains the complete browser source and anatomy assets. Open this folder in VS Code. To preview it, run the following command from this folder, then open http://localhost:8000/ in Chrome.

```sh
python3 -m http.server 8000
```

For GitHub Pages, upload the contents of this folder to the root of your repository. In **Settings → Pages**, publish from the root of your branch. The site uses relative asset paths and needs no build command.

## Source files

- `index.html` contains the interface, styles, source references, and atlas manifest.
- `assets/app.js` contains the procedure steps, camera controls, rendering shaders, and motion paths.
- `assets/loader.js` loads the six `assets/anatomy-*.bin` chunks. Together they form a gzip-compressed JSON array of mesh records. Each record's `data` field stores base64-encoded, little-endian float32 values, with three position and three normal components per vertex. Consecutive groups of three vertices form triangles.

To inspect or repack the anatomy records with Python 3, run the following from this folder.

```sh
python3 tools/anatomy.py unpack /tmp/pterional-meshes.json
python3 tools/anatomy.py pack /tmp/pterional-meshes.json
```

The atlas derives from Z-Anatomy (CC BY-SA 4.0), with upstream BodyParts3D attribution (DBCLS, CC BY-SA 2.1 Japan). See **Sources & model limits** in the guide for credits and the limits of the illustrative anatomy.
