# Atlas selection and extraction

Select the approach corridor and useful surrounding anatomy from the article before selecting meshes. Typical categories are superficial soft tissue, bone, outer dura and dural folds, neural tissue, ventricular system, arteries, veins, cranial/spinal nerves, and relevant tracts. Different approaches need different detail. Avoid loading an entire atlas where a regional subset suffices.

Look for locally supplied Z-Anatomy project archives or BodyParts3D OBJ archives in accessible source/download directories. Do not assume a particular username, source path or installed Blender. Discover available runtimes and read data without executing scripts bundled in downloaded archives. If network/source access is blocked, use an available licensed subset or explain missing structures; do not repeatedly request unavailable approvals.

## Z-Anatomy

Prefer Blender's supported export/data APIs when an available trusted installation can read the scene in background mode without executing archive scripts. Preserve each object's saved world matrix and original hierarchy, and verify any evaluated modifiers.

The bundled `readblend.py` is a fallback SDNA reader previously used successfully on a Z-Anatomy Blender 3.5 file. It is NOT a universal .blend evaluator. It supports that file's native mesh and curve storage; newer schemas may require adapting it. `atlas_catalog.py FILE.blend OUTPUT.json` lists objects without executing any embedded scene code.

The retained cranial meshes are a regional reference only. For a new region, catalog the actual atlas and write/adapt an exporter for its native schema, selected objects, coordinates and units. No complete atlas or universal region exporter is bundled.

Important extraction details:

- Source `Object.obmat` must be applied to every mesh and curve BEFORE a single shared display transform. Preserve left/right and superior/anterior axes explicitly. Negative determinant transforms require reversing triangle winding.
- Blender saves can reuse temporary old pointer addresses between mesh IDs. Resolve vertex/loop/polygon storage in the owning mesh's block scope, not a global address lookup alone. Check owner counts and exact buffer sizes. An exporter can otherwise appear to work but return wrong geometry or NaNs.
- `.g` / `.j` objects may be semantic label/join markers rather than tissue. Inspect geometry counts and types; do not treat marker lines as anatomical meshes.
- In the previously used schema, MVert positions, MLoop vertex indices, and MPoly loopstart/totloop form the base mesh. Triangulate carefully; a fan alone may fail on concave polygons. Base mesh export does not imply Blender display modifiers were evaluated.
- Vessels may be native Bézier curves. Tessellate cubic handles with interpolated source radii and bevel depth into tubes, then apply the object's world transform. A linear BPoint fallback is not accurate evaluation of arbitrary NURBS. Record approximations; do not silently call them exact.
- Keep the atlas coordinates shared across the whole regional subset; never center each object separately. Determine region center and common scale from the new case, not the reference exporter's cranial numbers.
- Original membranes/procedural layers can supplement missing atlas geometry, but describe them as illustrative. A red line on skull without a scalp mesh is an illustrative incision trajectory, not an actual incised scalp surface.

## BodyParts3D

Extract a relevant OBJ subset. Individual OBJ headers may include English names, FMA identifiers, source units, and attribution; inspect these before seeking a separate mapping. Preserve object coordinates, parse faces/indices/normals correctly, and triangulate as needed. Do not claim absent small structures simply because a broader parent organ is included.

## Credits and source quality

Use the license accompanying the actual downloaded files, and verify official source/license information when obtaining new datasets. Do not assume all Z-Anatomy objects use one license: unrelated contributed assets can differ. Retain upstream BodyParts3D attribution when applicable and comply with share-alike requirements for atlas derivatives. Keep license scope clear for article material, atlas derivatives, and original frontend/procedural illustration. Do not redistribute entire raw atlases within this skill.

Record source file/version/hash, object identifiers, source names, group, exact extraction/transform, and known omissions in the manifest. Use the source's anatomical specificity: neither merge important individual parts away nor invent a finer segmentation.
