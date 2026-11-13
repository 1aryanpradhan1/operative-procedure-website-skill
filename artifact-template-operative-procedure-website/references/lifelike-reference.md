# PR #1 feature and code reuse map

Use the bundled source from [pterional-craniotomy PR #1](https://github.com/nyuolab/pterional-craniotomy/pull/1), head `966eb1b5225768111bf7fe4300a6f14b916d01b7`, merged as `68be79e28960fa2697b63dff71f715cde1e4cbab`. The source files are copied from that revision, not recreated from its description. Consult `assets/source/reference-revision.json` for upstream SHA-256 hashes and intentional differences. Preserve this implementation when adapting a new procedure; replace only case-specific anatomy, content, geometry and controls required by the user's scope.

| Feature | Reuse from the reference | Adaptation constraints |
| --- | --- | --- |
| Tissue appearance | `assets/app.js`: `palettes`, `setPalette`, shaders in `initGL`; `assets/styles.css` | Keep Surgical as default and Atlas as an alternative, tissue-specific lighting, decorative texture, tone mapping and the low-precision fallback. Preserve palette persistence. Do not imply procedural texture is real microanatomy. |
| Ambient occlusion | Mesh normal magnitudes; `tools/anatomy_build/ao.py` | Normal direction is the surface normal; its length carries AO (0.3–1). Do not normalize stored buffers and discard this channel. Markers/instruments keep unit normals. |
| Scalp and closure | `scalp.py`, `buildSteps`, `surgicalState`, `incisionLine`, `innerColor` | Preserve skin/subcutaneous slab, galea, loose areolar gap and pericranium; progressive incision and separate galeal/skin closure. Fit to the actual procedure/side, not renamed pterional coordinates. |
| Flap motion | Vertex-shader curl and matching JavaScript `curlPoint`, flap/drape helpers | Preserve `flap = {key, pivot, axis, away, lift, radius, angle}`, rest-pose split passes, deformed normals, draping, labels, picking and depth sorting. Keep scalp, pericranial, fascial, temporalis and dural behavior coordinated with cumulative state and closure. |
| Tissue fit | `brain.py`, `dura.py`, `temporal_layers.py`, `veins.py`, `arachnoid.py` | Preserve native anatomy, conforming illustrative additions and documented limits. Keep the translucent arachnoid's picking behavior and stage-specific opening. Never silently present illustrations as segmentations. |
| Markings | `markers.py`, marker shaders, stage/arc-length reveal | Keep smooth constant-radius paths draped just above their own surface, outlines, minimum screen width, controlled depth bias and incision/suture timing. Adapt placement to each side. |
| Patient positioning | Pose transform/helpers, pose controls, `setSurgeonView`, orientation gizmo | Keep the anatomical/operative patient-pose toggle, sliders and schematic holder/table. Choose new defaults from evidence. Do not confuse patient pose with camera orientation. Preserve the deliberate Position-step demonstration. |
| Camera/input | Quaternion trackball, `rotateByDrag`, `rollView`, pointer and key handlers | Keep the upstream math but require Alt/Option for all manual rotation/roll. Ordinary drag/touch does not rotate. Keep pan/zoom and explicit presets. Remove the separate Operative View button and `setOperativeView` handler. |
| Data and build | Six anatomy chunks, `data/manifest.json`, loader, `tools/build_anatomy.py`, all `tools/anatomy_build/` modules | Preserve all fields and exact chunks for frontend-only edits. Keep source/license metadata. Materialization maps manifest/meshes into the existing packager and inlines the exact CSS. |

The pterional reference contains 650 records and 12 configurations of 27 steps. Those are revision facts, not requirements for a new guide. The manifest's `variants` snapshot must match `buildSteps`; update it if the procedure changes. Keep the initial research/PDF workflow and paper-to-step extraction in `research.md`.

## Intentional differences from the pull request

- Remove the dedicated Operative View button, handler, QA export and stale guide/manifest note that advertises it. Keep Patient Position and Surgeon's View, which are distinct features.
- Gate rotation/roll on the current event's Alt/Option modifier: Alt-drag uses the existing trackball instead of the upstream dial-roll gesture. Alt+arrows and Alt+Q/E retain keyboard rotation/roll. Two-pointer pan and zoom work without allowing an unmodified twist to roll. Plain drag is inert for rotation. Clear gestures on cancellation, lost capture and blur; suppress picking during modifier gestures.
- Update visible gesture help, accessible canvas instructions and reference documentation to match. Preserve the remaining renderer, geometry, CSS and build modules exactly.

## Geometry rebuilding

Do not rebuild anatomy for input, wording or styling changes. The shipped chunks already contain the PR geometry and AO. `tools/build_anatomy.py` is copied unchanged and needs NumPy/SciPy plus the original 614-record base from upstream commit `7961958`. That commit is not in the skill repository's history: use a full upstream clone or unpack its original chunks and supply `--base FILE`. Do not feed the already-derived 650 records back into this pipeline. The bundled full-atlas setup helper remains available for new regions.

Read `assets/source/README.md` for the upstream material, flap, marker and geometry contracts. Keep the same source limitations in adapted credits: scalp shells, straight hinges, venous courses, equipment, head pivot and procedural textures are illustrative; these are not patient-specific reconstructions or soft-tissue simulations.
