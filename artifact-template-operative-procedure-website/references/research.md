# Research and PDF intake

## Required intake state

First materialize the reference shell into a new empty project path. Then record the procedure, region, target/exposure, single-procedure versus requested family, requested option axes, known laterality, accessible atlas assets, source shortlist and PDF status in `research/intake.json` in the new project. Avoid an intake questionnaire when the named procedure and existing context resolve these. If the name covers materially different approaches and cannot be resolved by sources, ask one concise clarifying question while continuing independent research.

## Search and selection

Search current primary sources: original technical descriptions, cadaveric/microsurgical anatomy, technical notes, comparative technique studies, and relevant specialty guidance. Use primary publisher or PubMed/PMC metadata to verify titles, authors, years, DOI, corrections and access. A review can orient selection but is not evidence for a technique detail absent from the reviewed primary paper. Include a directly used secondary outline, such as Radiopaedia, in Papers; distinguish full-page access from an excerpt supplied by the user.

Build a small sufficient source set rather than a large decorative bibliography. It should cover the core sequence, relevant layers and landmarks, every selected alternative and the anatomy needed for the model. References for positioning and closure may differ from those for the central maneuver. No universal paper count is required. Do not transplant the reference website's 12-paper bibliography to a new procedure.

Read accessible full text before requesting it. Where access is missing, request PDFs with this practical structure:

- **Exact title — author, year.** DOI/article link. Needed for: specific exposure, tissue plane or variant. Priority: core or supplementary.

Group requests into a single message. Explain that figures are needed when modeling depends on them. Do not ask for the same PDF under several filenames. Match uploads by metadata/title/DOI and page content, not just filename. If all essential papers are already available, proceed without an artificial upload gate. If one essential PDF is still missing, continue supported portions and hold the dependent claims and geometry. Stop finalizing rather than silently inventing the unsupported portion.

## Extract the full operative record

Read each included paper from beginning to end and inspect every figure panel, caption, table, appendix, and relevant supplementary video or model. Track page and media coverage, including material that is unavailable, illegible, or outside scope. Use text extraction or OCR as an aid and verify important labels, units and spatial relationships visually.

For each paper, log all relevant findings with the source location and applicable technique or target. Capture positioning, fixation, surgeon and microscope orientation, landmarks and boundaries, distances and angles with units, tissue planes and order, instrument type and direction, procedural sequence, exposure limits, variants, structures at risk, safeguards, closure and relevant outcome limitations. Preserve conditional statements and negative findings. Separate directly reported detail, visual inference, and atlas approximation. Record conflicts and their resolution.

Give every finding a disposition in the working evidence map: represented in a specific website step, view, geometry, marking, or source note; retained as context; excluded with a reason; or awaiting evidence. Before delivery, reconcile the findings against the actual website and record what could not be represented. Extract and synthesize relevant information in your own words and preserve attribution.

## Verify the operative camera

Treat patient pose and operative camera as separate observations. Record head and body pose in the reported anatomical frame. From operative photographs or drawings, identify laterality, screen orientation, near and far landmarks, entry window and deep target, corridor direction, and structures expected to be visible. Document source figure and panel references and distinguish a photographed field from a schematic. Derive atlas camera direction from matched landmarks, choose screen orientation from the figure, and label inferred angles as illustrative. Use target- or stage-specific presets where the field changes materially. Verify both sides against identifiable landmark relationships and preserve anatomical occlusion. Log when the model lacks the segmentation or deformation needed to reproduce the paper's exposure.

## Evidence map

Record for each step/variant: source ID, PDF page and printed page if different, relevant figure or section, supported action, relevant structures, extent, purpose, alternatives and limitations. Link each modeled change to this map. Separate a paper's reported technique from its discussion of alternatives and from generic background anatomy. An abstract can establish scope or outcomes; it cannot establish an unseen dissection plane or instrument path.

A useful working record is:

```json
{"stepId":"expose-landmark","variantId":"standard","sources":[{"id":"technique-1","pdfPage":4,"figure":"2B","supports":"landmark exposure"}],"structures":["atlas-id"],"visualChange":"mark the exposed landmark","limits":["instrument direction is schematic"]}
```

Use exact case-specific values. A generic region mask is not evidence of a surgically measured opening. Resolve inconsistent naming by checking the papers and anatomy; do not quietly replace a user term with an assumed plane.

## Public source presentation

Guide cards read as a coherent educational guide: action and why, without author names, study comparisons, access notes or statements addressed to the creator. Papers holds the full curation list, verified citation, neutral short summary, source/DOI link and optional related-anatomy action. All listed sources should have contributed; show them all without a Relevant Only filter. Selected-configuration badges may vary, but do not hide the bibliography or put an extradural technique under a no-clinoidectomy applicability badge.

Do not show “supplied PDF,” “text available offline,” “PDF included in bundle,” or similar build provenance in the public cards. Keep access status privately in the evidence manifest. Do not add PDF download buttons. Supplied full text may be retained for the user's offline study consistent with its license; do not place complete paywalled text in a publicly deployable site without redistribution permission. The template's retained source is a private reference; strip or replace old case text and sources in the new website. Put article/atlas attribution in concise credits. A new study unavailable in full text remains explicitly limited in the working manifest and any affected public claim.
