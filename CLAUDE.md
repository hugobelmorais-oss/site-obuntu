# Claude Academic Research Skills

This repository is configured with the [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) skill suite for Claude Code.

## Available Skills

| Skill | Command | Description |
|-------|---------|-------------|
| Deep Research | `/deep-research` | Multi-agent research with source verification (Semantic Scholar, OpenAlex, Crossref, arXiv) |
| Academic Paper | `/academic-paper` | Full paper writing pipeline (~15,000 words, ~$4–6 in API cost) |
| Academic Paper Reviewer | `/academic-paper-reviewer` | Peer review system with 0-100 quality rubrics |
| Academic Pipeline | `/academic-pipeline` | Orchestrator that runs research → writing → review end-to-end |

## How It Works

On every session start, `.claude/hooks/SessionStart.sh` symlinks the four skills from `academic-research-skills/skills/` into `~/.claude/skills/`, making them available as slash commands.

## Requirements

- `ANTHROPIC_API_KEY` environment variable set
- Optional: `pandoc` and `tectonic` for DOCX/PDF output

## Source

Skills are cloned from `https://github.com/Imbad0202/academic-research-skills` into `academic-research-skills/`.
See that repo's [README](academic-research-skills/README.md) and [QUICKSTART](academic-research-skills/QUICKSTART.md) for full documentation.
