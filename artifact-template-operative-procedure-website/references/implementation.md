# Implementation and anatomy

## Start from the retained application

`assets/source/index.html`, its CSS, `assets/app.js`, loader and compressed anatomy chunks preserve the finished Pterional Craniotomy website. Do not rebuild a vaguely similar layout. Use `materialize_site.py` to copy it into a new project and expose editable `src/index.html`, `src/app.js` and JSON data. `baseline/` is the intact runnable reference, and `adaptation-status.json` identifies the original case. This baseline includes reference anatomy; it is not an atlas of every body region.

The script leaves the `<!-- GUIDE_DATA -->` and `<!-- GUIDE_RUNTIME -->` insertion markers in the editable HTML. The build helper reads `data/*.json`, renders the offline file, and produces a compressed static site and root-index ZIP. It does not infer a new operation from a procedure name. Do not use a successful unmodified reference build as a finished new procedure.

## Runtime adaptation map

Read the named parts of `src/app.js` before changing them. Reuse the rendering, stable-label and control infrastructure; replace the case-specific logic.

| Area | Reference implementation locations | Required adaptation |
| --- | --- | --- |
| Header and mobile layout | HTML body grid, `syncMobileLayout`, `updateMobileReaderHeight`, `updateMobilePanelHeight`, `alignActiveStep` | Preserve the tall mobile model and compact reader, move existing controls to the bottom dock/tab-adjacent navigation, and align the active card internally. If a single procedure removes the config row, update the body grid to `auto minmax(0,1fr)` rather than leaving a redundant row. |
| Variants | `config`, `configs`, `cname`, `mname`, `configName`, `choose`, top option inputs | One configuration by default; user-requested axes only for a family. Handle missing top inputs for a single procedure. |
| Sequence and state | `buildSteps`, `rebuild`, `activate`, `surgicalState` | New action sequence, source links, branch order, lasting prior actions and closure. Do not keep reference state names by accident. |
| Indications and Papers | `indicationGroups`, `chooseIndication`, `renderIndications`, `relevant`, `renderPapers`, `publicSummaries` | New indications, source applicability, focus targets and neutral summaries. Remove old full texts and references. |
| Layers and sides | `enabled`, `allEnabled`, `meshSide`, `operativeSide`, `relevantMesh`, `visible`, `meshOffset`, `toggleFullContext` | Region-specific categories and native paired IDs, context isolation, midline behavior, asymmetric anatomy, added illustrations. |
| Anatomy change | fragment shader in `initGL`, `surgicalState`, `changeKind`, `pointRetained` | New coordinates, opening/retraction geometry and highlight regions. Update CPU retention checks and GPU masks together. |
| Markings/instruments | meshes with `marker` or `instrument`, `follow`, `markerStages`, `stage`, marker shader uniforms | New surface-conforming paths, endpoints, instruments, timings, branch filters, mirrored or independently fitted additions. |
| Labels | `procedureLabelRegion`, `activeLabelMesh`, `candidatesForLabel`, `regionSurfaceAnchor`, `labelName`, `titleCase` | Relevant structure regions/anchors and abbreviation-preserving Title Case. Remove clinoid-specific targets. Adapt the abbreviation dictionary to the new region (e.g. PLL, ALL, ACDF, SCM, CN VII for a cervical case); preserve ordinary “All” control text and do not capitalize every atlas token indiscriminately. |
| 2D and context | `captureStepImages`, `showDiagram`, `updateChangeControls`, `zoomBy`, `project`, `draw`, pointer/wheel/key handlers | New tissue-plane diagram and actual selected side/context; preserve the complete state snapshot including `viewZoom`. Keep the same lens scale in GPU/picking and CPU label projection; do not replace the lens zoom with camera penetration. |
| Metadata | `data/manifest-data.json`, source/step/article/figure JSON files; credits in HTML | New title, papers, atlas transforms/licenses, schema counts, study plates, scope and limitations. |

Search for the old title, procedure names, fixed counts (12 / 27 / 614), pterion/sphenoid/clinoid/Sylvian, cranial offsets and hardcoded coordinates. Inspect each hit rather than deleting all cranial anatomy indiscriminately; some is legitimate context for another cranial operation. A default loader must derive expected mesh count from the current build, never assume 614. Update any QA hooks to match the new configuration schema.

## Geometry and source provenance

Use suitable native atlas geometry for the actual region. The bundled head subset can serve new cranial guides only where its source structures are actually appropriate. For spinal or other procedures, obtain a relevant licensed dataset or supplied anatomical meshes; do not stretch a skull or rename a vessel into another organ. Discover local atlases before downloading again. The `atlas-tools` folder has a PDF extractor, `.blend` catalog and fallback reader; consult its anatomy notes and adapt to the actual source format. It does not include an entire atlas. Missing source geometry remains a specific gap until resolved.

Preserve saved object world transforms followed by one common region transform and explicit units/axes. Verify winding, normals, triangle indices and all finite values. Native left structures are preferable to mirrored right structures. Added illustrative tissues may be mirrored only where appropriate; fit membranes independently to the native anatomy on each side. Record source IDs, transformation and whether each addition is native, reconstructed or schematic.

Do not fabricate clinical registration from an atlas. Named exact distances, bone landmarks and small deep apertures need source support and anatomical registration. When a segmentation lacks the required specificity, create an honest schematic illustration or identify the omission. Do not label a broad skull-base object as a separately reconstructed optic canal or strut.

## Physical depth and tissue fit

Use opaque, depth-tested surfaces with depth writes. Preserve actual geometric depth in every view: intact muscle lies outside intact bone, dura inside bone, and cortex inside dura where those tissues anatomically apply. A procedurally removed surface exposes what is underneath. Do not force a fixed semantic draw order that makes anatomy appear on top when rotated. Avoid transparency/sorting fixes that permit brain to show through intact bone. Inspect the full atlas context as well as the smaller operative subset.

Make openings and membranes clean, with stable borders and intentional thickness. Fit original fascia/fat layers to the actual muscle envelope and respect the correct lamina sequence. A superficial muscle elsewhere in the region must not be mistaken for the relevant deep temporalis or paraspinal envelope. Sample clearance at vertices and triangle interiors against the full nearby native cortex/bone or other surrounding structures on both sides; close rims and check for intersections. Sampling is useful evidence, not a continuous intersection proof.

Synchronize display, picking, highlight and label retention masks. A removed region must not remain pickable or anchor a label. Avoid stale pixel buffers and high-DPI coordinate errors. Keep the stable one-label box, local visible anchors and separate depth-aware picking framebuffer. For markers on a surface, use a small documented offset to prevent z-fighting, not a large floating trajectory. Never move all native anatomy to make labels or tools fit.

Fit membranes to the appropriate native atlas anatomy. The retained pterional dura is the October 30 local illustrative patch. Check membrane fit before and after opening and document coverage limits. Represent skin incisions with surface markings where relevant. Omit skin meshes and animated skin flaps.

## Time and branch behavior

Represent the procedure as cumulative state plus a current transition. A new step retains completed openings or displaced tissues. Before excludes the current transition, not all history. Closure reverses the appropriate opening/displacement while permanent resections stay removed. Place extradural work before dural opening and intradural work after it only when these are actually the new case's supported variants. Tools and trace markers should appear at their corresponding stages, disappear when unrelated, and follow the selected native side and the tissue they act on.

Use a staged tissue path that clears adjacent bone before sweeping along it. The retained temporalis lifts laterally, then moves inferiorly, and retraces the same path at closure. The retained bone flap illustrates an edge-first lift and lateral carry. Use case-supported lift and translation; omit generic flap rotations or hinge animations. Avoid openings that expand from the center to depict a removed flap. Use color highlights on the changed region and recommend a useful view without involuntarily replacing the user's current camera. Provide a clear full-context action when an isolated deep view is useful; describe the isolation as a display choice rather than additional tissue removal.

Use `setOperativeView` as the camera reset entry point. The pterional view uses Rodríguez Rubio et al. Figures 10C–D and 11 for field orientation and atlas landmarks for the line of sight. It mirrors laterality, puts the skull-base side at the top, and shifts the aim for basal steps. Apply the research reference's operative camera checks when adapting it. Leave step, tissue layers and comparison state intact.

## Packaging

`build_site.py` creates:

- `<slug>-anatomy-guide.html`: standalone offline page with embedded data/runtime;
- `site/index.html` and `site/assets/`: buildless hosted files;
- `<slug>-netlify.zip`: deployable contents with `index.html` at the ZIP root.

Data compression is lossless and split into 7 MiB pieces by default. Use current hosting documentation if destination limits matter. Keep website runtime assets in this ZIP; optional large GLB libraries, PDFs and working files belong in a separate study bundle. Do not discard needed geometry to shrink the upload without the user's request. The loader uses current-browser gzip decompression, reports progress and exposes an intelligible failure message. Check decoded data against source data. Revalidate new/deployment-specific code; the reference's prior checks do not prove a changed case works.

## Added assets

Put new local image, font, audio or video assets under project `static/`, with paths matching their site URL (for example `static/assets/plane.svg` is `assets/plane.svg`). The build helper copies these files into the hosted site and embeds matching references in the offline HTML, runtime and JSON data. Keep frontend code/styles inline in `src/index.html` and `src/app.js`; do not add unbundled module/CSS/script dependencies. Source assets outside this documented folder or unknown relative dependencies must be embedded explicitly or resolved before building. Do not store anatomy PDFs or secrets in `static/`, which is public deployment content.

Exact quoted media URLs (including literal backtick strings) and root-relative media URLs can be embedded. Computed/dynamic asset paths must be resolved to embedded data explicitly; do not assume the packager can evaluate JavaScript. Publish only the generated `site/` directory, never the whole working project or its private `baseline/`, evidence or PDF folders.

## Retained mobile implementation

At widths up to 760 px the reference uses `100dvh`, a dynamically measured reading row and a flexible model row. `syncMobileLayout` moves existing layer/reset controls into `mobileModelDock` and the existing pager into `mobileStepNav`; it restores their desktop homes above that breakpoint. `updateMobileReaderHeight` measures a hidden active-card probe containing the title and first two sentences. `alignActiveStep` adjusts only the guide panel scroll position, and mobile bottom padding permits the last card to align. A layout ResizeObserver and resize handler recompute the allocation. The upward menu is aligned to the dock rather than its narrower summary, and its viewport budget has no artificial minimum. Default mobile labels are disabled independently of desktop preference, while explicit selection remains available. Adapt these mechanisms for the new case without reintroducing the removed mobile title/status/preset controls. These are source and software-test observations; actual phone rendering still needs permitted browser/device inspection.
