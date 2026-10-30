# Thailand’s 4PW: Journal club

[Read the presentation](https://smartwoo.github.io/4pw-journal-club/?route=story&mode=read&scene=JC01&step=1) · [Present](https://smartwoo.github.io/4pw-journal-club/?route=story&mode=present&scene=JC01&step=1) · [Explore the CLD](https://smartwoo.github.io/4pw-journal-club/?route=story&mode=present&scene=JC-CLD-STORY&step=1)

**Bridging the Policy-Implementation Gap in Thailand’s Participatory Public Policy Process Based on Wisdom (4PW): A Realist and Systems Thinking Synthesis Through Collaborative Governance and Social Participation Lenses**

A research proposal and qualified synthesis, organised around Why, Concepts, Design, Lenses, Findings and Discussion. The main route has 22 pages, with a complete 56-page evidence library. Each content page presents a question, a Thai key conclusion, supporting points and source links. The CLD explorer retains 24 variables, 50 relationships and 28 named loop views, with relationship-level evidence and qualifications.

The CLD builds on one growing canvas, connecting R1 to R2 and onward through shared variables. Names appear before new arrows; polarity, delays and source evidence remain inspectable. The main walkthrough introduces each relationship once in 107 steps. The detailed 187-step route also retraces reused relationships. Use Current path or zoom to read individual loops within the final network overview.

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
