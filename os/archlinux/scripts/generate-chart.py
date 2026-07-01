#!/usr/bin/env python3
"""
generate-chart.py — Reads manifest.yaml and generates a Mermaid dependency diagram.

Usage:
    python generate-chart.py                         # Print Mermaid to stdout
    python generate-chart.py --inject README.md      # Inject into README between markers
    python generate-chart.py --validate              # Validate all module files exist
    python generate-chart.py --packages              # Generate package list markdown
    python generate-chart.py --html chart.html       # Generate interactive HTML visualization

The Mermaid diagram uses:
    - Subgraphs for phases (colored)
    - Rounded rectangles for required modules
    - Hexagons for optional modules
    - Stadiums for recommended modules
    - Dashed subgraphs for profiles
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PHASE_STYLES = {
    "phase-0": {"fill": "#1a1a2e", "stroke": "#e94560"},
    "phase-1": {"fill": "#16213e", "stroke": "#0f3460"},
    "phase-2": {"fill": "#1a1a2e", "stroke": "#533483"},
    "phase-3": {"fill": "#0f3460", "stroke": "#e94560"},
    "phase-4": {"fill": "#533483", "stroke": "#e94560"},
}

PHASE_ICONS = {
    "phase-0": "📋",
    "phase-1": "🖥️",
    "phase-2": "🛡️",
    "phase-3": "🪟",
    "phase-4": "🚀",
}

INJECT_START = "<!-- CHART:START -->"
INJECT_END = "<!-- CHART:END -->"

# ---------------------------------------------------------------------------
# Manifest Loading
# ---------------------------------------------------------------------------

def load_manifest(manifest_path: Path) -> dict:
    """Load and return the manifest YAML."""
    with open(manifest_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def collect_all_modules(manifest: dict) -> list[dict]:
    """Flatten all modules from all phases (including profile modules)."""
    modules = []
    for phase in manifest.get("phases", []):
        for mod in phase.get("modules", []):
            mod["_phase_id"] = phase["id"]
            mod["_phase_name"] = phase["name"]
            modules.append(mod)

        for profile in phase.get("profiles", []):
            for mod in profile.get("modules", []):
                mod["_phase_id"] = phase["id"]
                mod["_phase_name"] = phase["name"]
                mod["_profile_id"] = profile["id"]
                mod["_profile_name"] = profile["name"]
                modules.append(mod)

        # Shared modules at phase level (outside profiles)
        if "modules" in phase and "profiles" in phase:
            # Already handled above — shared modules are in phase["modules"]
            pass

    return modules


# ---------------------------------------------------------------------------
# Mermaid Generation
# ---------------------------------------------------------------------------

def _node_shape(mod: dict) -> tuple[str, str]:
    """Return (open_bracket, close_bracket) based on required status."""
    req = mod.get("required", "optional")
    if req is True or req == "true":
        return ("([", "])")          # Stadium (pill) = required
    elif req == "recommended":
        return ("([", "])")          # Stadium = recommended
    else:
        return ("{{", "}}")          # Hexagon = optional


def _sanitize_id(module_id: str) -> str:
    """Make a safe Mermaid node ID."""
    return module_id.replace("-", "_")


def generate_mermaid(manifest: dict, for_html: bool = False) -> str:
    """Generate a Mermaid flowchart from the manifest."""
    lines = ["flowchart TD"]
    all_modules = collect_all_modules(manifest)
    module_ids = {m["id"] for m in all_modules}

    for phase in manifest.get("phases", []):
        pid = phase["id"]
        pname = phase["name"]
        icon = PHASE_ICONS.get(pid, "📦")
        lines.append(f"")
        lines.append(f'    subgraph {_sanitize_id(pid)}["{icon} Phase: {pname}"]')

        # Non-profile modules
        phase_modules = phase.get("modules", [])
        for mod in phase_modules:
            sid = _sanitize_id(mod["id"])
            ob, cb = _node_shape(mod)
            lines.append(f'        {sid}{ob}"{mod["name"]}"{cb}')

        # Profiles
        for profile in phase.get("profiles", []):
            prof_id = _sanitize_id(profile["id"])
            lines.append(f'        subgraph {prof_id}["{profile["name"]}"]')
            for mod in profile.get("modules", []):
                sid = _sanitize_id(mod["id"])
                ob, cb = _node_shape(mod)
                lines.append(f'            {sid}{ob}"{mod["name"]}"{cb}')
            lines.append(f"        end")

        lines.append(f"    end")

    # Edges (prerequisites)
    lines.append(f"")
    lines.append(f"    %% Prerequisites")
    for mod in all_modules:
        sid = _sanitize_id(mod["id"])
        for prereq in mod.get("prerequisites", []):
            if prereq in module_ids:
                lines.append(f"    {_sanitize_id(prereq)} --> {sid}")

    # Styles
    lines.append(f"")
    lines.append(f"    %% Phase Styles")
    for pid, style in PHASE_STYLES.items():
        sid = _sanitize_id(pid)
        lines.append(
            f'    style {sid} fill:{style["fill"]},stroke:{style["stroke"]},color:#fff'
        )

    # Click interactions for HTML rendering
    if for_html:
        lines.append(f"")
        lines.append(f"    %% Interactive click links")
        for mod in all_modules:
            sid = _sanitize_id(mod["id"])
            # The HTML file is generated in the root of the archlinux directory,
            # so the relative path from the HTML file to the markdown file matches mod["file"]
            lines.append(f'    click {sid} "{mod["file"]}" "Open {mod["name"]} module"')

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Package List Generation
# ---------------------------------------------------------------------------

def generate_package_list(manifest: dict) -> str:
    """Generate a markdown package list grouped by phase and profile."""
    lines = [
        "# Master Package List",
        "",
        "> Auto-generated from `manifest.yaml`. Do not edit manually.",
        "",
    ]

    for phase in manifest.get("phases", []):
        lines.append(f"## {phase['name']}")
        lines.append("")
        lines.append("| Module | Packages | Required |")
        lines.append("|--------|----------|----------|")

        for mod in phase.get("modules", []):
            pkgs = ", ".join(f"`{p}`" for p in mod.get("packages", [])) or "—"
            req = mod.get("required", "optional")
            if req is True:
                req_str = "✅ Required"
            elif req == "recommended":
                req_str = "⚡ Recommended"
            else:
                req_str = "💡 Optional"
            lines.append(f"| {mod['name']} | {pkgs} | {req_str} |")

        for profile in phase.get("profiles", []):
            lines.append(f"")
            lines.append(f"### Profile: {profile['name']}")
            lines.append("")
            lines.append("| Module | Packages | Required |")
            lines.append("|--------|----------|----------|")
            for mod in profile.get("modules", []):
                pkgs = ", ".join(f"`{p}`" for p in mod.get("packages", [])) or "—"
                req = mod.get("required", "optional")
                if req is True:
                    req_str = "✅ Required"
                elif req == "recommended":
                    req_str = "⚡ Recommended"
                else:
                    req_str = "💡 Optional"
                lines.append(f"| {mod['name']} | {pkgs} | {req_str} |")

        lines.append("")

    # Summary
    all_modules = collect_all_modules(manifest)
    all_pkgs = set()
    for mod in all_modules:
        all_pkgs.update(mod.get("packages", []))
    all_pkgs.discard("")

    lines.append("---")
    lines.append("")
    lines.append(f"**Total unique packages:** {len(all_pkgs)}")
    lines.append("")
    lines.append("**Full list (alphabetical):**")
    lines.append("```")
    lines.append(" ".join(sorted(all_pkgs)))
    lines.append("```")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_manifest(manifest: dict, base_path: Path) -> list[str]:
    """Validate that all module files exist and prerequisites are valid."""
    errors = []
    all_modules = collect_all_modules(manifest)
    module_ids = {m["id"] for m in all_modules}

    for mod in all_modules:
        # Check file exists
        file_path = base_path / mod["file"]
        if not file_path.exists():
            errors.append(f"MISSING FILE: {mod['id']} -> {mod['file']}")

        # Check prerequisites reference valid modules
        for prereq in mod.get("prerequisites", []):
            if prereq not in module_ids:
                errors.append(f"INVALID PREREQ: {mod['id']} depends on '{prereq}' (not found)")

    return errors


# ---------------------------------------------------------------------------
# README Injection
# ---------------------------------------------------------------------------

def generate_html(mermaid_block: str, manifest: dict, output_path: Path) -> None:
    """Generate a standalone HTML file with interactive Mermaid.js rendering."""
    all_modules = collect_all_modules(manifest)
    total_pkgs = set()
    for mod in all_modules:
        total_pkgs.update(mod.get("packages", []))
    total_pkgs.discard("")

    # Build stats per phase
    phase_stats = []
    for phase in manifest.get("phases", []):
        mods = list(phase.get("modules", []))
        for profile in phase.get("profiles", []):
            mods.extend(profile.get("modules", []))
        required = sum(1 for m in mods if m.get("required") is True or m.get("required") == "true")
        recommended = sum(1 for m in mods if m.get("required") == "recommended")
        optional = len(mods) - required - recommended
        phase_stats.append({
            "name": phase["name"],
            "total": len(mods),
            "required": required,
            "recommended": recommended,
            "optional": optional,
            "milestone": phase.get("milestone", ""),
        })

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arch Linux Guide — Dependency Map</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0d1117;
            color: #e6edf3;
            font-family: 'Segoe UI', Inter, -apple-system, sans-serif;
            min-height: 100vh;
        }}
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            padding: 2rem 3rem;
            border-bottom: 1px solid #30363d;
        }}
        .header h1 {{
            font-size: 1.8rem;
            font-weight: 600;
            background: linear-gradient(90deg, #e94560, #533483);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        .header p {{ color: #8b949e; font-size: 0.95rem; }}
        .stats-bar {{
            display: flex;
            gap: 1rem;
            padding: 1rem 3rem;
            background: #161b22;
            border-bottom: 1px solid #21262d;
            overflow-x: auto;
        }}
        .stat-card {{
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 0.8rem 1.2rem;
            min-width: 180px;
            flex-shrink: 0;
        }}
        .stat-card h3 {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #8b949e;
            margin-bottom: 0.3rem;
        }}
        .stat-card .number {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #e94560;
        }}
        .stat-card .detail {{
            font-size: 0.7rem;
            color: #6e7681;
            margin-top: 0.2rem;
        }}
        .legend {{
            display: flex;
            gap: 1.5rem;
            padding: 0.8rem 3rem;
            background: #161b22;
            border-bottom: 1px solid #21262d;
            font-size: 0.8rem;
            color: #8b949e;
            flex-wrap: wrap;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}
        .legend-shape {{
            width: 24px;
            height: 16px;
            border-radius: 8px;
            border: 2px solid;
        }}
        .legend-shape.required {{ border-color: #e94560; background: rgba(233,69,96,0.15); }}
        .legend-shape.recommended {{ border-color: #533483; background: rgba(83,52,131,0.15); }}
        .legend-shape.optional {{
            border-color: #6e7681;
            background: rgba(110,118,129,0.1);
            clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
            border-radius: 0;
        }}
        .chart-container {{
            padding: 2rem;
            display: flex;
            justify-content: center;
            overflow: auto;
            min-height: 60vh;
        }}
        .mermaid {{
            max-width: 100%;
        }}
        .mermaid svg {{
            max-width: none !important;
        }}
        .controls {{
            position: fixed;
            bottom: 1.5rem;
            right: 1.5rem;
            display: flex;
            gap: 0.5rem;
            z-index: 100;
        }}
        .controls button {{
            background: #21262d;
            border: 1px solid #30363d;
            color: #e6edf3;
            padding: 0.5rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: background 0.2s;
        }}
        .controls button:hover {{ background: #30363d; }}
        .footer {{
            padding: 1rem 3rem;
            border-top: 1px solid #21262d;
            color: #6e7681;
            font-size: 0.75rem;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Arch Linux Installation Guide — Dependency Map</h1>
        <p>Interactive visualization of {len(all_modules)} modules across {len(manifest.get('phases', []))} phases &middot; {len(total_pkgs)} unique packages</p>
    </div>

    <div class="stats-bar">
""" + "".join(f"""
        <div class="stat-card">
            <h3>{s['name']}</h3>
            <div class="number">{s['total']}</div>
            <div class="detail">{s['required']} required &middot; {s['recommended']} recommended &middot; {s['optional']} optional</div>
            <div class="detail" style="color:#8b949e;margin-top:4px">{s['milestone']}</div>
        </div>
""" for s in phase_stats) + f"""
        <div class="stat-card">
            <h3>Total</h3>
            <div class="number">{len(all_modules)}</div>
            <div class="detail">{len(total_pkgs)} unique packages</div>
        </div>
    </div>

    <div class="legend">
        <div class="legend-item"><div class="legend-shape required"></div> Required</div>
        <div class="legend-item"><div class="legend-shape recommended"></div> Recommended</div>
        <div class="legend-item"><div class="legend-shape optional"></div> Optional</div>
    </div>

    <div class="chart-container">
        <pre class="mermaid">
{mermaid_block}
        </pre>
    </div>

    <div class="controls">
        <button onclick="resetZoom()">Reset View</button>
        <button onclick="toggleFullscreen()">Fullscreen</button>
    </div>

    <div class="footer">
        Generated from <code>manifest.yaml</code> by <code>generate-chart.py --html</code>
    </div>

    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark',
            themeVariables: {{
                primaryColor: '#1a1a2e',
                primaryTextColor: '#e6edf3',
                primaryBorderColor: '#e94560',
                lineColor: '#6e7681',
                secondaryColor: '#16213e',
                tertiaryColor: '#0f3460',
                fontSize: '14px',
            }},
            flowchart: {{
                curve: 'basis',
                padding: 20,
                htmlLabels: true,
                useMaxWidth: false,
            }},
        }});

        function resetZoom() {{
            const container = document.querySelector('.chart-container');
            container.scrollTo(0, 0);
        }}

        function toggleFullscreen() {{
            const el = document.querySelector('.chart-container');
            if (!document.fullscreenElement) {{
                el.requestFullscreen().catch(() => {{}});
            }} else {{
                document.exitFullscreen();
            }}
        }}
    </script>
</body>
</html>"""

    output_path.write_text(html, encoding="utf-8")
    print(f"HTML chart written to {output_path}")


def inject_into_readme(readme_path: Path, mermaid_block: str) -> None:
    """Replace content between CHART:START and CHART:END markers in a README."""
    content = readme_path.read_text(encoding="utf-8")

    if INJECT_START not in content or INJECT_END not in content:
        print(f"ERROR: Markers {INJECT_START} / {INJECT_END} not found in {readme_path}", file=sys.stderr)
        sys.exit(1)

    before = content[: content.index(INJECT_START) + len(INJECT_START)]
    after = content[content.index(INJECT_END) :]

    new_content = f"{before}\n\n```mermaid\n{mermaid_block}\n```\n\n{after}"
    readme_path.write_text(new_content, encoding="utf-8")
    print(f"Injected chart into {readme_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate dependency chart from manifest.yaml")
    parser.add_argument("--manifest", default="manifest.yaml", help="Path to manifest.yaml")
    parser.add_argument("--inject", metavar="README", help="Inject Mermaid into README between markers")
    parser.add_argument("--html", metavar="FILE", help="Generate standalone HTML visualization")
    parser.add_argument("--validate", action="store_true", help="Validate all module files exist")
    parser.add_argument("--packages", action="store_true", help="Generate package list markdown")
    parser.add_argument("--packages-output", metavar="FILE", help="Write package list to file")

    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: Manifest not found: {manifest_path}", file=sys.stderr)
        sys.exit(1)

    manifest = load_manifest(manifest_path)
    base_path = manifest_path.parent

    if args.validate:
        errors = validate_manifest(manifest, base_path)
        if errors:
            print(f"Found {len(errors)} error(s):", file=sys.stderr)
            for err in errors:
                print(f"  ❌ {err}", file=sys.stderr)
            sys.exit(1)
        else:
            all_modules = collect_all_modules(manifest)
            print(f"✅ All {len(all_modules)} modules validated successfully.")
            sys.exit(0)

    if args.packages:
        pkg_md = generate_package_list(manifest)
        if args.packages_output:
            Path(args.packages_output).write_text(pkg_md, encoding="utf-8")
            print(f"Package list written to {args.packages_output}")
        else:
            print(pkg_md)
        sys.exit(0)

    if args.html:
        mermaid = generate_mermaid(manifest, for_html=True)
        generate_html(mermaid, manifest, Path(args.html))
    elif args.inject:
        mermaid = generate_mermaid(manifest, for_html=False)
        inject_into_readme(Path(args.inject), mermaid)
    else:
        mermaid = generate_mermaid(manifest, for_html=False)
        print(mermaid)


if __name__ == "__main__":
    main()
