# Thailand’s 4PW: Journal club

[Read the presentation](https://smartwoo.github.io/4pw-journal-club/?route=story&mode=read&scene=JC01&step=1) · [Present](https://smartwoo.github.io/4pw-journal-club/?route=story&mode=present&scene=JC01&step=1) · [Explore the CLD](https://smartwoo.github.io/4pw-journal-club/?route=story&mode=present&scene=JC-CLD-STORY&step=1)

**Bridging the Policy-Implementation Gap in Thailand’s Participatory Public Policy Process Based on Wisdom (4PW): A Realist and Systems Thinking Synthesis Through Collaborative Governance and Social Participation Lenses**

A research proposal and qualified synthesis, organised around Why, Concepts, Design, Lenses, Findings and Discussion. The main route has 22 pages, with a complete 56-page evidence library. Each content page presents a question, a Thai key conclusion, supporting points and source links. The revised CLD contains 49 variables (12 stocks, 23 flows, 14 converters), 66 causal links, 24 stock–flow connections and 35 named loops.

The CLD follows the supplied revision exactly: 35 loop starts, all 237 ordered relationship steps including reused links, 35 closures, 14 remaining connections and one final overview, for 322 steps. Both presentation routes use this same walk. The default Loop by loop view builds each circular loop one relationship at a time, moving from R1 to R2 after closure. Reused links appear when their step is reached; the loop code and name enter the centre only after closure. Growing network remains available for the cumulative map. Use zoom to inspect the final overview.

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
