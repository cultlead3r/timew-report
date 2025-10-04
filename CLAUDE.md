# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a simple Python-based time tracking report generator. It reads JSON time interval data from stdin and generates an HTML report table.

## Commands

### Generate Report
```bash
cat input.json | ./report.py > output.html
```

The script expects JSON input with the following structure:
```json
[
  {
    "start": "2025-10-02T15:37:00Z",
    "end": "2025-10-02T15:56:00Z",
    "tags": ["LA"],
    "annotation": "bypass cache for login"
  }
]
```

## Architecture

**report.py**: Single-file script that:
- Reads JSON array of time intervals from stdin
- Parses ISO 8601 timestamps (handles "Z" suffix)
- Calculates duration in hours for completed intervals
- Outputs HTML table with columns: Start, End, Tags, Annotation, Duration (h)
- Handles open intervals (no end time) by displaying "Open" and "-" for duration
