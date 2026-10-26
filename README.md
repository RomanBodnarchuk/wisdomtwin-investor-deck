# WisdomTwin investor deck mirror

Current approved artifact: **E10.1, October 16, 2026**.
SHA-256: `d96d87fea85aa2349e2ed3c2d6258f446c664fc50a3d6420d72486c5c69a2919`.
21 pages, 238282 bytes. Source approval and retrieval evidence remain in AI-HQ.

## Public entry points
- index.html and the legacy deck-e10.html route embed WisdomTwin-Investor-Deck.pdf.
- invest/index.html links to the same canonical PDF.
- Every existing PDF filename is retained as a compatibility alias with exactly the same E10.1 bytes, including older date/version filenames. Those filenames do not identify historical content.
- No forms, gate policies, booking settings, agent knowledge or other websites are changed.

## Verification
Run `python3 verify_release.py` before release.
After publishing, download every served PDF and compare its SHA-256 against the value above. Check desktop/mobile viewing, direct download and investor overview navigation.
A repository check does not prove that Netlify or GitHub Pages has deployed the change.

## Rollback
Original source files and per-file hashes are retained privately at:
The private October 26 AI-HQ release evidence (not included in this public repository)
Current production base commit: bacf5211dab3bd6853f5e73ee07cbc3e34e2adc1.
Preserve that deployment for rollback. No historical source assets are deleted from version history.
