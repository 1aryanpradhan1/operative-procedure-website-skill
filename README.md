# Operative procedure website skill

A Codex skill that builds interactive anatomy guides from operative papers. The repository includes the working pterional reference, its regional meshes, and the site build tools. A setup script fetches the full Z-Anatomy atlas from a pinned upstream revision when the requested procedure needs other anatomy.

## Install and start

1. Clone this repository or download its ZIP from GitHub. Copy the `artifact-template-operative-procedure-website` folder into `~/.codex/skills/`. If you use a custom `CODEX_HOME`, use its `skills/` directory. Reopen Codex if the skill is not listed.
2. Open a project folder where Codex can save the guide. Start with a prompt such as:

   > Use $artifact-template-operative-procedure-website to build a guide to the left retrosigmoid approach. Cover the standard exposure through closure.

   A procedure name is enough to start. Include a target, side, or variant if you already know it.

## What happens next

1. **Paper intake.** Codex finds relevant technique and anatomy papers and reads the full texts it can access. It asks in one list for the specific PDFs it still needs, with links and what each paper will resolve.
2. **Attach PDFs.** Upload the requested PDFs in the same Codex chat, including operative figures or supplements if requested. Reply, for example, “Here are the PDFs. Continue building the guide.” If the papers are already accessible, Codex can proceed without an upload.
3. **Build and review.** Codex resumes the saved project, maps the paper findings to the operative steps and geometry, loads the relevant anatomy, and checks the rendered guide. You receive editable website files, a deployment ZIP, and notes on any evidence or anatomy gaps.

## Anatomy and software

- Use Python 3.11 or newer for the bundled setup and build scripts, and a current WebGL browser to preview the guide.
- The pterional reference loads from the meshes already in the skill. When those meshes are insufficient, Codex can fetch the full atlas with `scripts/setup_atlas.py` from inside the skill folder. It downloads about 83 MiB, checks the archive checksum, and extracts only `Startup.blend`. You can also run this ahead of time:

  ```sh
  python3 scripts/setup_atlas.py --cache ~/anatomy-atlas/z-anatomy
  ```

  If you already have the pinned `Z-Anatomy.zip`, add `--archive /path/to/Z-Anatomy.zip`. Tell Codex the cache path if you set it up yourself.
- For extracting and evaluating new meshes, the skill prefers a compatible Blender installation with scene script execution disabled. It includes a fallback catalog reader for the pinned scene. If the atlas lacks a structure or the paper does not establish the geometry, Codex will identify that gap and ask for appropriate meshes or evidence.

See the [upstream atlas](https://github.com/Z-Anatomy/Models-of-human-anatomy) and the skill’s reference attribution for the anatomy sources and license terms. Article transcriptions are excluded from this repository.

## Updated reference and interaction

The bundled website now uses the actual code and assets from [pterional-craniotomy PR #1](https://github.com/nyuolab/pterional-craniotomy/pull/1), commit `966eb1b5225768111bf7fe4300a6f14b916d01b7`: Surgical/Atlas tissue shading, baked ambient occlusion, layered scalp, progressive incision and closure, curling/peeling flaps, conforming membranes and surface-following landmarks. It retains Patient Position, Surgeon's View and the orientation gizmo.

The dedicated **Operative View** button is removed. **Hold Alt/Option and drag to rotate**; ordinary drag/touch stays fixed. Alt/Option + arrows rotates and Alt/Option + Q/E rolls. Wheel/pinch zoom and Shift/right-drag or two-finger pan remain available. Reset View and explicit presets still work. The Position step retains its deliberate patient-positioning demonstration.

Paper discovery, full-text/PDF intake, figure inspection and evidence mapping remain the first steps. The skill includes the upstream renderer and geometry code, rather than instructions to approximate their appearance. `assets/source/reference-revision.json` (inside the skill folder) records the source revision, exact upstream hashes and the small local differences. The materializer supports the new external manifest and stylesheet; both hosted and standalone builds preserve the same anatomy and rendering.
