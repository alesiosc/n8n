# Fork: NQM OCR Automation (WIP)

This branch is an **incomplete but functional** work-in-progress for automating TradingView level updates.

### ✅ What It Does So Far
- Opens browser tabs and UI menus
- Verifies the "NQM2025" label is present using OCR
- If not found, retries up to 5 times and aborts if still missing
- Highlights and copies level text
- Pastes levels into TradingView indicators using simulated triple-click + Ctrl+A + Ctrl+V fallback
- Includes appropriate delays between steps for timing-sensitive actions

### 🚧 Not Yet Complete
- Doesn't handle ES, SPX, QQQ, SPY workflows yet
- No generalized zone selection logic for other symbols
- Still needs a screenshot logging fallback for failed OCR (optional)

### 🧠 Next Steps (for next fork)
- Build a looped symbol handler (NQM2025 → ESM2025 → etc.)
- Refactor click management into named actions or grouped steps
- Add visual logging for OCR failures (e.g. save to `/logs/failed_NQM.png`)
- Eventually merge into a broader multi-symbol indicator updater

---
**Status:** This is a frozen snapshot of working progress. Use as a base for fork-nqm-runner-v2 and beyond.
