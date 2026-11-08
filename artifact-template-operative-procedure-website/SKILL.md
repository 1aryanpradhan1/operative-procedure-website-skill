---
name: artifact-template-operative-procedure-website
description: Build operative procedure websites by adapting the bundled Pterional Craniotomy interface, anatomy and operative sequence using primary technique sources. Deliver editable static website source with interactive 3D and 2D views, laterality, layers and procedure markings.
---

# Operative Procedure Website

Start from the working Pterional Craniotomy site in `assets/source/`. Use it as the reference for the interface and implemented behaviors. Adapt the site to the requested procedure and scope. Reuse matching pterional anatomy, steps and geometry where applicable. Replace case-specific content and geometry for other procedures. Add only the variants the user requests.

## 1. Research first, then request PDFs

Read [research and source handling](references/research.md). Materialize a new project shell with the helper described in section 3 before saving intake there; this shell preparation does not establish a new procedure. Resume an existing materialized project on later PDF uploads instead of materializing into it again. Identify the named procedure, anatomical region, intended extent and any variants the user explicitly wants. A single procedure is the default. Do not invent top-level option groups. For a requested procedure family, derive the option axes from the user's scope and evidence; clarify only consequential ambiguity.

Find primary operative technique and microsurgical anatomy papers, verify their bibliographic identities and full-text access, and request the specific missing PDFs in one concise prioritized list. Give titles, authors/year, DOI or article link, and what each will resolve. Use accessible full text directly and recognize PDFs already supplied. Do not ask the user to upload an obtainable open-access PDF again. Ask for additional figure pages only when an uploaded file actually lacks them.

**Pause evidence-dependent final step writing and geometric reconstruction while required PDFs are missing.** A research shortlist and the reusable shell can be prepared during this phase. Keep a saved intake/source-status file so the next upload resumes the same project. Do not substitute abstracts, guessed dimensions or a different technique for missing operative evidence. Once the needed PDFs arrive, continue autonomously through the build and review; another approval round is unnecessary.

## 2. Inspect the papers and plan the procedure

Read the complete supplied technique PDFs and visually inspect the pages containing operative photographs, diagrams, instrument positions and tissue planes. Use an available PDF workflow. Source diagrams inform anatomy and geometry; reproducing published figures on the website is optional, not required. Create original 2D views and markings by default.

Complete the paper-by-paper extraction and disposition audit in the research reference, then make a source-to-step evidence map and procedure plan before modeling. Carry forward every relevant supported detail into the model, steps, views, or supporting source notes. Keep page/figure anchors, evidence limits, source applicability and disagreements in working data. Full-text access is not proof that a particular step, variant or measurement is supported.

Use **one meaningful operative action or anatomical transition per step**, at the granularity of the reference's 27-step positioning-to-closure sequence. Read [the interface and content contract](references/website-contract.md). Match density and importance, not a fixed count: a simpler procedure can need fewer steps and a more complex one more. Do not compress an entire exposure into one card or pad it with trivial actions. Each card has an action title and 2–4 short sentences explaining what happens, the relevant anatomy, and why. Keep study names, citations and user-specific provenance out of Guide prose.

## 3. Adapt the working website

Read [implementation and anatomy](references/implementation.md). If the project was not already materialized during intake, use `scripts/materialize_site.py --skill-dir <this-skill> --output <new-empty-project>` to copy and unpack the retained source into an editable project. Work on the copy. Preserve the reference CSS and controls instead of scaffolding a visually different site. The helper also retains the working baseline for comparison. Never edit the skill's reference assets during use.

Review every case-specific sequence, indication, paper, source text, label anchor, atlas selection, anatomical transform, mask, instrument placement and marking. Replace each item that does not fit the requested scope. The copied runtime is a pterional implementation; its coordinates and clinical logic are **reference code**, not a universal surgery engine. Follow the adaptation map and implement the new procedure's geometry and state machine explicitly.

For a single procedure, remove the top variant selectors and omit model counts; retain the title, side/context and normal model controls. For a requested family, show clearly labeled top selectors and generate every supported requested combination. Do not carry over the example's 12-model count or its clinoidectomy / temporalis / Sylvian choices. Represent evidence-limited combinations honestly in Papers/Indications; do not imply that selectable combinations have been clinically validated.

Keep Right / Left / Both context, camera and zoom persistence, a side-aware Operative View camera reset derived from operative figures and corridor landmarks, paired Relevant / All layer controls, one stable Title Case label, 2D views, procedural markings, visible instruments, Before / After and Replay behavior. Mobile starts with automatic labels off; selecting a surface can still show one label. Mobile step navigation stays beside the tabs, and each active step aligns directly beneath them. For procedures where sidedness has no anatomical meaning, preserve context controls without inventing a different mirrored procedure. Keep the Instruments checkbox in Layers & View as the sole instruments toggle. Keep unmanipulated anatomy such as brain, arteries and nerves enabled in the recommended view where applicable and let opaque anatomy occlude it. Preserve cumulative removal or reflection. See the detailed contract.

## 4. Verify with an independent reviewer

Read [verification and review](references/verification.md). Run syntax, data, state/branch, laterality, geometry and interaction checks appropriate to the new case. Inspect the actual website in a permitted browser when available; never bypass a browser-access denial or call a software projection a browser screenshot.

After the website is complete, use a separate review agent when available to inspect the whole site against the supplied papers and this contract, including every variant and both sides. Have it report concrete inconsistencies and fix them in the working project, with bounded ownership of edits. Recheck affected behavior. If delegation is unavailable, perform the same audit and state that review was not independent. Avoid claiming perfection, clinical validation, or successful live rendering without evidence.

## 5. Deliver

Use `scripts/build_site.py --project <project> --output <new-output-directory>` to create an offline HTML and a buildless deployment folder/ZIP after adaptation. The build helper preserves complete geometry and splits compressed data into small files; it is not an anatomy generator or validation substitute. Check the source provenance, atlas licenses, output consistency and ZIP integrity. Reuse `assets/source/atlas-tools` only when relevant to the chosen dataset.

Deliver a complete editable static site with root `index.html`, all runtime/anatomy assets and a source ZIP ready for GitHub Pages or Netlify. Include a local HTTP preview and VS Code instructions. Include the build helper’s standalone offline guide and summarize verification and known limitations. Include separate 3D model exports if requested; interactive website configurations must work even without external GLB downloads. Keep working data and developer notes out of the public interface. Do not publish merely because the template was invoked: deployment follows the user's requested destination and authorization.
