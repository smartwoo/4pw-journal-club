# Thailand’s 4PW: Journal club

[Read the presentation](https://smartwoo.github.io/4pw-journal-club/?route=story&mode=read&scene=JC01&step=1) · [Present](https://smartwoo.github.io/4pw-journal-club/?route=story&mode=present&scene=JC01&step=1) · [Explore the CLD](https://smartwoo.github.io/4pw-journal-club/?route=story&mode=present&scene=JC-CLD-STORY&step=1)

**Bridging the Policy-Implementation Gap in Thailand’s Participatory Public Policy Process Based on Wisdom (4PW): A Realist and Systems Thinking Synthesis Through Collaborative Governance and Social Participation Lenses**

A research proposal and qualified synthesis, organised around Why, Concepts, Design, Lenses, Findings and Discussion. The main route has 22 pages, with a complete 56-page evidence library. Each content page presents a question, a Thai key conclusion, supporting points and source links. The revised CLD contains 49 variables (12 stocks, 23 flows, 14 converters), 66 causal links, 24 stock–flow connections and 35 named loops.

The CLD follows the supplied revision exactly: 35 loop starts, all 237 ordered relationship steps including reused links, 35 closures, 14 remaining connections and one final overview, for 322 steps. Both presentation routes use this same walk. The default Build the full map view retains R1 as R2 grows from shared variables, then accumulates every later loop. A new connection appears only when both endpoint variables have been introduced; reused connections are highlighted at their next narrative step. Each current loop is named from its first frame: its code appears on the diagram and its full name appears in the caption. A dashed code glyph indicates a loop being assembled; at closure it becomes solid and gains its full name underneath. The circular glyph, code and full name form one black annotation inside the loop’s open interior. Adaptive wrapping keeps titles complete, and completed annotations remain with the accumulated map. The final overview contains all 35 named loop markers and a clickable list. One loop at a time remains available as an optional focused view. Use Fit for the accumulated map, ซูมวงนี้ for the current loop, or the zoom/pan controls for detail.

Follow each relationship is a third view. Each loop starts with its English title, a complete upcoming-loop overview, a guiding question and a truthful bridge from the existing map. Next follows each ordered relationship with its full curve, endpoint labels, polarity and delay in view. The closure returns to the loop overview, uses its supplied Thai title, and retains the full supplied Thai/English synthesis. A large source → (+/−) target reading strip keeps names readable on long arcs and opens the original evidence drawer. Fit returns to the current frame after manual zoom, pan or loop inspection. Share this view with `cldView=relationship` in the URL.

Opening overviews mark preview-only objects separately; they do not change introduced counts, source order, reveal clocks or the completed-loop count. Detailed steps return to the exact source prefix. Shared relationships remain highlighted when they belong to the current loop; unrelated paths, variables and loop annotations fade to gray. The final overview restores the complete map’s colors and black loop names. Opening questions orient the walkthrough; they do not replace or rewrite the supplied closing synthesis.

All 35 loops follow the supplied Thai/English summaries and 237 step-by-step causal explanations. The reader and loop drawers retain the original version, revised title and summary, and bilingual causal steps. Display codes are numbered within R/B classes in story order; original canonical IDs remain in the evidence trace. The original model labels and relationship order remain unchanged. Written causal expressions consistently use A → (+) B or A → (−) B; graphic arrows retain their conventional adjacent polarity symbols. Growing connections follow round circular and elliptical branches, with new variables placed around established loops in source order. One unnamed tail relationship uses a compact convex arch. Geometry is prepared in advance so earlier curves remain stable as later loops appear. Circular glyph direction follows the directed loop around its own annotation region, independently of R/B classification. The head at twelve o’clock points right for clockwise and left for counterclockwise; a focused loop uses the direction of its separate circular layout.

[Read the current model specification](https://smartwoo.github.io/4pw-journal-club/model-specification.html). This generated public reader preserves the model sequence and explains evidence boundaries. The 16 added causal links remain analogical proposals. Of the 50 original ledger endpoint/sign signatures, 49 match the revision and AA5 changes its target; the simplified old diagram was a separate projection. Signature agreement, stock–flow accounting and structural closure do not constitute causal validation.

The presentation distinguishes proposed methods, source findings, provisional model relationships and conditional implications. A closed diagram does not establish observed causal feedback. Original figures retain their attribution and licence; unpublished participant-level records are not distributed.

## Updating the public edition

Build the latest working deck locally:

```powershell
python .\site\build_public_site.py --check
python .\site\build_public_site.py
```

The script reads the latest `4PW-journal-club_preview.html`, writes a separate `site/dist/index.html`, and copies only the nine abstract PNGs and four attributed source-figure JPGs requested by the page. It never edits the working HTML. No licensed font binaries, work folders, downloaded papers, raw attachments or original model/manuscript files are copied.

After the chosen GitHub repository is connected and Pages uses GitHub Actions, run `./site/Publish-Latest.ps1` from the project folder to rebuild the public edition and push it. The workflow deploys the update to the same URL. `-BuildOnly` rebuilds without Git or publishing. The script checks that Git is isolated to this `site` folder and stages only the reviewed public bundle and deployment files. It never stages the broader research project.

The public copy replaces local-file links with an accessible explanation of unpublished study materials. It omits participant-level consultation records and source locators, unused raw candidate abstracts and machine paths. Recorded contribution counts and support/review-depth labels remain the original ledger assessments, with an explicit redaction notice; they are not recalculated evidence. Published APA links remain unchanged.

Review the public edition before publishing, including the fallback fonts on a device without the owner's installed fonts, source notes, evidence drawers, the CLD explorer, Print and both Read/Present modes. `public-build-audit.json` is a local build report, not a web asset.

For a repository whose root is this `site` folder, commit only the intended deployment sources and `dist/`; the provided workflow publishes `dist/`. The original working deck is outside the repository and is not a CI input. Rebuild locally after approved changes and commit the updated `dist/`. Keep the same repository and Pages URL so existing `?mode=...&scene=...&step=...` links continue to work. The release notice offers a reload when `version.json` changes; it does not interrupt a running presentation.

Do not commit the broader project folder, `work/`, attachment exports or font files. Repository creation, Git credentials and Pages configuration are handled separately.
