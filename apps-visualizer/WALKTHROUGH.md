# Play Store App AI Impact Visualizer — Walkthrough

## What Was Built

An interactive treemap visualizer for **318 Play Store apps** scored for AI impact (1–10), modeled after the [jobs-master] US Job Market Visualizer.

### Files Created

| File | Purpose |
|------|---------|
| [build_app_data.py]( | Merges 3 CScore JSONs → `data.json` with categories + Play Store URLs |
| [apps-visualizer/index.html] | Single-file interactive treemap visualizer |
| [apps-visualizer/data.json]| Flat JSON with 318 app entries |

### Key Features

- **Treemap** grouped by 22 Play Store categories (Education, AI Assistant, Productivity, etc.)
- **3 color layers**: AI Impact Score (green→red), Disruption Type (4 colors), Confidence (green/yellow/red)
- **Stats dashboard** with histograms, tier breakdowns, and cross-charts that update per layer
- **Rich tooltips** showing app name, category, score bar, disruption type, confidence, key drivers, and reasoning
- **Play Store linking** — click any tile to search for it on Google Play

## How to Run

```bash
cd apps-visualizer && python3 -m http.server 8001
# Open http://localhost:8001
```

