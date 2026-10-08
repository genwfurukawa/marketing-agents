#!/usr/bin/env python3
"""Brand enforcement for edited videos. One schema for every client.

The brand lives in the client's config.yaml under `visual_style` (the same block
brand_image_generator.py reads). Paths in it are relative to the config's repo root
(the directory holding config.yaml).

Subcommands:
  check    config.yaml                 validate the brand block; diff against source CSS if set
  install  config.yaml PROJECT         copy fonts/logos into a HyperFrames project, write
                                       brand/brand.css, brand/brand.lock.json and DESIGN.md
  compose  config.yaml PROJECT ...     write index.html: video + captions + lower third +
                                       logo bug + end card, all from brand roles
  lint     PROJECT                     fail on any color, font or logo not in the brand lock
"""
import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("needs PyYAML (python3 -m pip install pyyaml)")

GENERIC_FAMILIES = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
                    "inherit", "initial", "unset", "-apple-system", "blinkmacsystemfont"}
NAMED_COLORS = {"black": "#000000", "white": "#FFFFFF", "red": "#FF0000", "blue": "#0000FF",
                "green": "#008000", "yellow": "#FFFF00", "gray": "#808080", "grey": "#808080",
                "orange": "#FFA500", "purple": "#800080", "pink": "#FFC0CB", "navy": "#000080",
                "silver": "#C0C0C0", "lime": "#00FF00", "cyan": "#00FFFF", "magenta": "#FF00FF"}
REQUIRED_ROLES = ["bg", "surface", "text", "text-on-surface", "muted", "accent", "accent-text",
                  "highlight-bg", "highlight-text", "border"]
REQUIRED_FONTS = ["display", "body"]
REQUIRED_LOGOS = ["on-dark", "on-light"]


def norm_hex(h):
    h = h.strip().upper()
    if re.fullmatch(r"#[0-9A-F]{3}", h):
        h = "#" + "".join(c * 2 for c in h[1:])
    if re.fullmatch(r"#[0-9A-F]{8}", h):
        h = h[:7]  # alpha suffix: judge the base color
    return h


def rgb_to_hex(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(int(float(r)), int(float(g)), int(float(b)))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


# ---------------------------------------------------------------- load + check

def load(config_path):
    cfg_path = Path(config_path).expanduser().resolve()
    cfg = yaml.safe_load(cfg_path.read_text()) or {}
    vs = cfg.get("visual_style") or {}
    return cfg_path.parent, cfg, vs


def problems(root, cfg, vs):
    errs, warns = [], []
    palette = {k: norm_hex(v) for k, v in (vs.get("palette") or {}).items()}
    if not palette:
        errs.append("visual_style.palette is missing (the full color token set)")
    for name, hexv in palette.items():
        if not re.fullmatch(r"#[0-9A-F]{6}", hexv):
            errs.append(f"palette.{name} = {hexv!r} is not a hex color")
    roles = vs.get("roles") or {}
    for r in REQUIRED_ROLES:
        if r not in roles:
            errs.append(f"roles.{r} missing")
        elif roles[r] not in palette:
            errs.append(f"roles.{r} = {roles[r]!r} is not a palette name")
    fonts = vs.get("fonts") or {}
    for f in REQUIRED_FONTS:
        if f not in fonts:
            errs.append(f"fonts.{f} missing")
    for role, spec in fonts.items():
        if not spec.get("files"):
            errs.append(f"fonts.{role} ({spec.get('family')}) has no files; renders would substitute a font")
        for ff in spec.get("files", []):
            if not (root / ff["src"]).exists():
                errs.append(f"fonts.{role}: file not found {ff['src']}")
    logos = vs.get("logo_files") or {}
    for l in REQUIRED_LOGOS:
        if l not in logos:
            errs.append(f"logo_files.{l} missing")
    for name, rel in logos.items():
        p = root / rel
        if not p.exists():
            errs.append(f"logo_files.{name}: file not found {rel}")
        elif p.suffix.lower() == ".svg":
            txt = p.read_text(errors="ignore")
            fills = {norm_hex(x) for x in re.findall(r"(?:fill|stroke)\s*[:=]\s*\"?(#[0-9A-Fa-f]{3,8})", txt)}
            if not fills and "class=" in txt:
                errs.append(f"logo_files.{name}: SVG sets no fill (renders black by default)")
            for fl in fills - set(palette.values()):
                errs.append(f"logo_files.{name}: SVG color {fl} is not in the palette")
    for k, v in (vs.get("colors") or {}).items():  # legacy keys for the image generator
        if norm_hex(v) not in palette.values():
            errs.append(f"colors.{k} = {v} is not in the palette (image generator would drift)")
    video = vs.get("video") or {}
    for k in ("captions", "logo_bug", "end_card"):
        if k not in video:
            warns.append(f"video.{k} missing; defaults will be used")

    src = vs.get("source_css")
    if src:
        css_path = (root / src).resolve()
        if not css_path.exists():
            errs.append(f"source_css not found: {css_path}")
        else:
            prefix = vs.get("source_css_prefix", "--")
            css = css_path.read_text()
            m = re.search(r":root\s*{([^}]*)}", css)
            tokens = dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9A-Fa-f]{3,8})", m.group(1) if m else ""))
            for var, val in tokens.items():
                name = var[len(prefix):] if var.startswith(prefix) else var
                if name not in palette:
                    errs.append(f"source CSS defines {var}: {val} but palette has no '{name}'")
                elif palette[name] != norm_hex(val):
                    errs.append(f"palette.{name} = {palette[name]} but source CSS {var} = {norm_hex(val)}")
            for name in palette:
                if f"{prefix}{name}" not in tokens:
                    warns.append(f"palette.{name} is not in source CSS (brand addition, or stale?)")
            fams = set(re.findall(r"--font-[\w-]+\s*:\s*\"([^\"]+)\"", m.group(1) if m else ""))
            for role, spec in fonts.items():
                if spec["family"] not in fams:
                    errs.append(f"fonts.{role} = {spec['family']} is not a primary font in source CSS")
    return errs, warns


def cmd_check(args):
    root, cfg, vs = load(args.config)
    errs, warns = problems(root, cfg, vs)
    for w in warns:
        print(f"warn: {w}")
    for e in errs:
        print(f"FAIL: {e}")
    print(f"{'FAIL' if errs else 'PASS'}: {len(errs)} errors, {len(warns)} warnings ({args.config})")
    sys.exit(1 if errs else 0)


# ---------------------------------------------------------------- install

def brand_css(vs):
    palette = {k: norm_hex(v) for k, v in vs["palette"].items()}
    out = ["/* generated by brand.py install; do not edit, change visual_style in config.yaml */"]
    for role, spec in vs["fonts"].items():
        for ff in spec["files"]:
            out.append("@font-face{font-family:\"%s\";src:url(\"fonts/%s\") format(\"woff2\");"
                       "font-weight:%s;font-style:%s;font-display:block}"
                       % (spec["family"], Path(ff["src"]).name, ff.get("weight", "400"), ff.get("style", "normal")))
    root = [f"--c-{k}:{v}" for k, v in palette.items()]
    root += [f"--brand-{r}:var(--c-{p})" for r, p in vs["roles"].items()]
    for role, spec in vs["fonts"].items():
        root.append(f"--font-{role}:\"{spec['family']}\",{spec.get('fallback', 'sans-serif')}")
    shape = vs.get("shape") or {}
    root += [f"--brand-radius:{shape.get('radius_px', 0)}px",
             f"--brand-border:{shape.get('border_px', 4)}px",
             f"--brand-shadow:{shape.get('shadow_px', 12)}px"]
    out.append(":root{" + ";".join(root) + "}")
    for role, spec in vs["fonts"].items():
        tt = "uppercase" if spec.get("case") == "uppercase" else "none"
        wt = f";font-weight:{spec['weight']}" if spec.get("weight") else ""
        out.append(f".font-{role}{{font-family:var(--font-{role});text-transform:{tt}{wt}}}")
    return "\n".join(out) + "\n"


def design_md(vs, name):
    palette = {k: norm_hex(v) for k, v in vs["palette"].items()}
    lines = [f"# {name}: brand for this video (generated by brand.py, do not edit)", "",
             "Use ONLY these values. Reference them as CSS variables from `brand/brand.css`",
             f"(`var(--brand-accent)`, `var(--c-{next(iter(palette))})`, `var(--font-body)`), never as raw hex",
             "or font names. `brand.py lint` fails the render on anything else.", "",
             "## Colors (palette)", ""]
    lines += [f"- `--c-{k}` {v}" for k, v in palette.items()]
    lines += ["", "## Roles", ""]
    lines += [f"- `--brand-{r}` = {p} ({palette[p]})" for r, p in vs["roles"].items()]
    lines += ["", "## Fonts", ""]
    for role, spec in vs["fonts"].items():
        lines.append(f"- {role}: {spec['family']} (`var(--font-{role})`, class `.font-{role}`)"
                     + (", always uppercase" if spec.get("case") == "uppercase" else ""))
    shape = vs.get("shape") or {}
    lines += ["", "## Shape", "",
              f"- Corners: {shape.get('radius_px', 0)}px. Borders: {shape.get('border_px', 4)}px solid "
              f"var(--brand-border). Shadows: hard offset {shape.get('shadow_px', 12)}px, no blur.", "",
              "## Logos", ""]
    lines += [f"- {k}: `brand/logos/{Path(v).name}`" for k, v in vs["logo_files"].items()]
    lines += ["", "Captions, lower third, logo bug and end card are generated by `brand.py compose`.",
              "Add scenes on top, but style them only with the variables above."]
    return "\n".join(lines) + "\n"


def cmd_install(args):
    root, cfg, vs = load(args.config)
    errs, _ = problems(root, cfg, vs)
    if errs:
        for e in errs:
            print(f"FAIL: {e}")
        sys.exit("brand block is invalid; fix config.yaml (run `brand.py check`) before installing")
    proj = Path(args.project)
    (proj / "brand" / "fonts").mkdir(parents=True, exist_ok=True)
    (proj / "brand" / "logos").mkdir(parents=True, exist_ok=True)
    lock = {"client": cfg.get("client", {}).get("name") if isinstance(cfg.get("client"), dict) else None,
            "config": str(Path(args.config).expanduser().resolve()),
            "palette": {k: norm_hex(v) for k, v in vs["palette"].items()},
            "families": sorted({s["family"] for s in vs["fonts"].values()}),
            "logos": {}, "video": vs.get("video") or {}, "roles": vs["roles"],
            "fonts": {r: {"family": s["family"], "case": s.get("case", "none"), "weight": s.get("weight")}
                      for r, s in vs["fonts"].items()},
            "logo_files": {k: f"brand/logos/{Path(v).name}" for k, v in vs["logo_files"].items()}}
    for spec in vs["fonts"].values():
        for ff in spec["files"]:
            shutil.copy2(root / ff["src"], proj / "brand" / "fonts" / Path(ff["src"]).name)
    for k, rel in vs["logo_files"].items():
        dst = proj / "brand" / "logos" / Path(rel).name
        shutil.copy2(root / rel, dst)
        lock["logos"][f"brand/logos/{dst.name}"] = sha(dst)
    (proj / "brand" / "brand.css").write_text(brand_css(vs))
    (proj / "brand" / "brand.lock.json").write_text(json.dumps(lock, indent=1))
    name = (cfg.get("client") or {}).get("name") if isinstance(cfg.get("client"), dict) else None
    (proj / "DESIGN.md").write_text(design_md(vs, name or vs.get("name") or "Brand"))
    print(f"installed brand into {proj}: {len(lock['palette'])} colors, {len(lock['families'])} font families, "
          f"{len(lock['logos'])} logos")


# ---------------------------------------------------------------- compose

def probe(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:format=duration", "-of", "json", str(video)],
                         check=True, capture_output=True, text=True).stdout
    d = json.loads(out)
    s = d["streams"][0]
    return float(d["format"]["duration"]), s["width"], s["height"]


def region_luma(video, dur, vw, vh, x, y, w, h, samples=12):
    """Mean luma (0-255) of a source-pixel region, sampled across the video."""
    step = max(dur / samples, 0.5)
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video), "-vf",
         f"fps=1/{step:.3f},crop={int(w)}:{int(h)}:{int(x)}:{int(y)},signalstats,"
         "metadata=print:key=lavfi.signalstats.YAVG:file=-", "-f", "null", "-"],
        capture_output=True, text=True).stdout
    vals = [float(l.split("=")[1]) for l in out.splitlines() if "YAVG=" in l]
    return sum(vals) / len(vals) if vals else 0.0


def caption_groups(words, max_words, max_gap):
    groups, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w["start"] - cur[-1]["end"] > max_gap):
            groups.append(cur)
            cur = []
        cur.append(w)
        if re.search(r"[.?!]$", w["text"]):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def sub_doc(comp_id, W, H, style, body, tl_lines):
    """A HyperFrames sub-composition: everything the render needs lives inside <template>."""
    return f"""<!doctype html>
<html>
  <head><meta charset="UTF-8" /><!-- generated by brand.py compose; restyle via config.yaml visual_style --></head>
  <body>
    <template>
      <style>
        #root {{ position: absolute; inset: 0; }}
{style}
      </style>
      <div id="root" data-composition-id="{comp_id}" data-width="{W}" data-height="{H}">
        {body}
      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
        {chr(10).join('        ' + t for t in tl_lines).strip()}
        window.__timelines["{comp_id}"] = tl;
      </script>
    </template>
  </body>
</html>
"""


def cmd_compose(args):
    proj = Path(args.project)
    lock = json.loads((proj / "brand" / "brand.lock.json").read_text())
    v = lock["video"]
    cap, lt, bug, end = (v.get("captions") or {}), (v.get("lower_third") or {}), \
        (v.get("logo_bug") or {}), (v.get("end_card") or {})
    video = Path(args.video)
    if video.resolve().parent != proj.resolve():
        shutil.copy2(video, proj / video.name)
    dur, vw, vh = probe(proj / video.name)
    portrait = vh > vw
    W, H = (1080, 1920) if portrait else (1920, 1080)
    end_s = float(end.get("seconds", 4.0)) if not args.no_end_card else 0.0
    total = round(dur + end_s, 3)
    safe = int((v.get("safe_zone_px") or {}).get("landscape", 96))
    cta = args.cta if args.cta is not None else end.get("cta", "")
    url = args.url if args.url is not None else end.get("url", "")
    logos = lock["logo_files"]
    have = lambda role: role if role in lock["fonts"] else "body"   # brands may skip mono/editorial
    upper = lambda role: "uppercase" if lock["fonts"].get(have(role), {}).get("case") == "uppercase" else "none"
    weight = lambda role, default: lock["fonts"].get(have(role), {}).get("weight") or default
    comp_dir = proj / "compositions"
    comp_dir.mkdir(exist_ok=True)
    for old in comp_dir.glob("brand-*.html"):
        old.unlink()
    hosts, notes = [], []

    def host(cid, start, length, track):
        hosts.append(f'<div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                     f'data-start="{start:.3f}" data-duration="{length:.3f}" data-track-index="{track}" '
                     f'data-width="{W}" data-height="{H}"></div>')

    # captions: one track, one group visible at a time, active word via data-on
    if not args.no_captions:
        words = json.loads(Path(args.transcript).read_text())
        size = int(cap.get("size_px", 58)) if not portrait else 64
        bottom = int(cap.get("bottom_px", 96)) if not portrait else 520
        x0, x1 = (float(v) for v in args.caption_region.split(",")) if args.caption_region else (0.0, 1.0)
        left_px, right_px = max(safe, int(x0 * W)), max(safe, int((1 - x1) * W))
        style = f"""        .cap {{ position: absolute; left: {left_px}px; right: {right_px}px; bottom: {bottom}px; width: fit-content;
                max-width: {W - left_px - right_px}px; margin: 0 auto; text-align: center; line-height: 1.25;
                font-family: var(--font-{have(cap.get('font', 'body'))}); font-weight: {int(cap.get('weight', 800))};
                font-size: {size}px; text-transform: {upper(cap.get('font', 'body'))};
                color: var(--brand-{cap.get('text', 'text')});
                background: color-mix(in srgb, var(--brand-{cap.get('box', 'bg')}) {int(float(cap.get('box_opacity', 0.82)) * 100)}%, transparent);
                padding: 14px 26px; border-radius: var(--brand-radius); }}
        .w {{ padding: 0 6px; border-radius: var(--brand-radius); }}
        .w[data-on="1"] {{ background: var(--brand-highlight-bg); color: var(--brand-highlight-text); }}"""
        groups, tl = [], []
        for gi, g in enumerate(caption_groups(words, int(cap.get("max_words", 5)), float(cap.get("max_gap_s", 0.6)))):
            gs, ge = max(0.0, g[0]["start"]), min(g[-1]["end"] + 0.25, dur)
            if groups and gs < groups[-1][1]:  # never two groups on screen
                groups[-1][1] = gs
            if ge - gs < 0.2:
                continue
            groups.append([gs, ge, gi, g])
        body = []
        for gs, ge, gi, g in groups:
            spans = []
            for wi, w in enumerate(g):
                wid = f"c{gi}w{wi}"
                spans.append(f'<span class="w" id="{wid}">{html.escape(w["text"])}</span>')
                tl.append(f'tl.set("#{wid}", {{attr: {{"data-on": "1"}}}}, {max(w["start"], gs):.3f});')
                tl.append(f'tl.set("#{wid}", {{attr: {{"data-on": "0"}}}}, {min(w["end"], ge):.3f});')
            body.append(f'<div id="cap{gi}" class="clip cap" data-start="{gs:.3f}" data-duration="{ge - gs:.3f}" '
                        f'data-track-index="1">{" ".join(spans)}</div>')
        (comp_dir / "brand-captions.html").write_text(
            sub_doc("brand-captions", W, H, style, "\n        ".join(body), tl))
        host("brand-captions", 0.0, dur, 2)
        notes.append(f"{len(groups)} caption groups")

    if args.name:
        ls, ld = float(lt.get("start_s", 1.0)), float(lt.get("duration_s", 5.0))
        nf, tf = have(lt.get("name_font", "display")), have(lt.get("title_font", "mono"))
        style = f"""        #lt {{ position: absolute; left: {int(lt.get('left_px', safe))}px;
                bottom: {int(lt.get('bottom_px', 220)) if not portrait else 900}px;
                background: var(--brand-surface); color: var(--brand-text-on-surface);
                border: var(--brand-border) solid var(--brand-border);
                border-left: 18px solid var(--brand-accent);
                box-shadow: var(--brand-shadow) var(--brand-shadow) 0 var(--brand-border);
                padding: 22px 34px 20px 30px; }}
        .lt-name {{ display: block; font-family: var(--font-{nf}); font-weight: {weight(nf, 400)}; font-size: 46px; line-height: 1.05;
                text-transform: {upper(nf)}; }}
        .lt-title {{ display: block; font-family: var(--font-{tf}); font-size: 22px; font-weight: 600;
                letter-spacing: .14em; margin-top: 10px; color: var(--brand-muted); text-transform: {upper(tf)}; }}"""
        title = f'<span class="lt-title">{html.escape(args.title)}</span>' if args.title else ""
        body = f'<div id="lt"><span class="lt-name">{html.escape(args.name)}</span>{title}</div>'
        tl = ['tl.from("#lt", {x: -80, opacity: 0, duration: 0.5, ease: "power3.out"}, 0);',
              f'tl.to("#lt", {{x: -80, opacity: 0, duration: 0.4, ease: "power2.in"}}, {ld - 0.45:.3f});']
        (comp_dir / "brand-lower-third.html").write_text(sub_doc("brand-lower-third", W, H, style, body, tl))
        host("brand-lower-third", ls, ld, 3)
        notes.append("lower third")

    if end_s:
        style = f"""        #end {{ position: absolute; inset: 0; background: var(--brand-bg); display: flex;
                flex-direction: column; align-items: center; justify-content: center; gap: 56px; }}
        .end-logo {{ height: {150 if not portrait else 110}px; }}
        .end-cta {{ font-family: var(--font-{have('display')}); font-weight: {weight('display', 400)}; font-size: 44px; text-transform: {upper('display')};
                background: var(--brand-accent); color: var(--brand-accent-text); padding: 26px 44px;
                border: var(--brand-border) solid var(--brand-accent-text);
                box-shadow: var(--brand-shadow) var(--brand-shadow) 0 var(--brand-surface); }}
        .end-url {{ font-family: var(--font-{have('mono')}); font-size: 28px; letter-spacing: .16em;
                text-transform: {upper('mono')}; color: var(--brand-text); }}"""
        logo = logos.get(end.get("logo", "on-dark"), logos["on-dark"])
        body = (f'<div id="end"><img class="end-logo" src="{logo}" alt="">'
                + (f'<div class="end-cta">{html.escape(cta)}</div>' if cta else "")
                + (f'<div class="end-url">{html.escape(url)}</div>' if url else "") + "</div>")
        tl = ['tl.from("#end .end-logo", {y: 40, opacity: 0, duration: 0.5, ease: "power3.out"}, 0.1);']
        if cta:
            tl.append('tl.from("#end .end-cta", {y: 40, opacity: 0, duration: 0.5, ease: "power3.out"}, 0.3);')
        if url:
            tl.append('tl.from("#end .end-url", {opacity: 0, duration: 0.5}, 0.5);')
        (comp_dir / "brand-end-card.html").write_text(sub_doc("brand-end-card", W, H, style, body, tl))
        host("brand-end-card", dur, end_s, 5)
        notes.append("end card")

    vert, horiz = bug.get("corner", "top-right").split("-")
    m = int(bug.get("margin_px", 56))
    # pick the logo variant that reads against the footage under it
    bh = int(bug.get("height_px", 40))
    bw = bh * 6 + 40
    sx, sy = vw / W, vh / H
    rx = (W - m - bw) if horiz == "right" else m - 20
    ry = m - 20 if vert == "top" else (H - m - bh - 20)
    luma = region_luma(proj / video.name, dur, vw, vh, max(0, rx * sx), max(0, ry * sy), bw * sx, (bh + 40) * sy)
    variant = bug.get("logo") if args.logo_variant == "config" else (
        args.logo_variant if args.logo_variant != "auto" else ("on-light" if luma > 140 else "on-dark"))
    bug_logo = logos.get(variant, logos["on-dark"])
    notes.append(f"logo bug {variant} (footage luma {luma:.0f}/255 under it)")
    doc = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="brand/brand.css" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: var(--brand-bg); }}
      body {{ font-family: var(--font-body); color: var(--brand-text); }}
      #a-roll {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #brand-logo-bug {{ position: absolute; {vert}: {m}px; {horiz}: {m}px;
              height: {int(bug.get('height_px', 40))}px; opacity: {float(bug.get('opacity', 0.95))}; }}
    </style>
  </head>
  <body>
    <!-- generated by brand.py compose; brand elements live in compositions/brand-*.html -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}">
      <video id="a-roll" class="clip" src="{video.name}" playsinline data-start="0" data-duration="{dur:.3f}"
        data-track-index="0" data-has-audio="true"></video>
      <img id="brand-logo-bug" class="clip" src="{bug_logo}" alt="" data-start="0" data-duration="{dur:.3f}" data-track-index="4">
      {chr(10).join('      ' + h for h in hosts).strip()}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (proj / "index.html").write_text(doc)
    print(f"wrote {proj / 'index.html'} + compositions/brand-*.html: {W}x{H}, {total}s "
          f"({dur:.1f}s video + {end_s}s end card); {', '.join(notes) or 'video only'}")


# ---------------------------------------------------------------- lint

def cmd_lint(args):
    proj = Path(args.project)
    lock_path = proj / "brand" / "brand.lock.json"
    if not lock_path.exists():
        sys.exit("FAIL: no brand/brand.lock.json; run `brand.py install <config.yaml> <project>` first")
    lock = json.loads(lock_path.read_text())
    allowed = set(lock["palette"].values())
    families = {f.lower() for f in lock["families"]}
    errs, warns = [], []
    files = [p for p in proj.rglob("*") if p.suffix in (".html", ".css", ".js")
             and "node_modules" not in p.parts and p.relative_to(proj).parts[0] != "brand"]
    for f in files:
        rel = f.relative_to(proj)
        for ln, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            if "cdn.jsdelivr" in line or line.strip().startswith(("//", "<!--")):
                continue
            for m in re.finditer(r"#[0-9A-Fa-f]{8}\b|#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b", line):
                # skip id selectors like #c1w2 / #a-roll: a color is followed by ; , ) " ' space or end
                before = line[:m.start()]
                if re.search(r"(src|href|id)=[\"'][^\"']*$", before):
                    continue
                if norm_hex(m.group()) not in allowed:
                    errs.append(f"{rel}:{ln} color {m.group()} is not a brand color")
            for m in re.finditer(r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)", line):
                if rgb_to_hex(*m.groups()) not in allowed:
                    errs.append(f"{rel}:{ln} color {m.group()}) is not a brand color")
            for m in re.finditer(r"hsla?\(", line):
                errs.append(f"{rel}:{ln} hsl() color; use a brand variable")
            for m in re.finditer(r"(?:color|background(?:-color)?|border(?:-color)?|fill|stroke)\s*:\s*([a-z]+)\b", line, re.I):
                name = m.group(1).lower()
                if name in NAMED_COLORS and NAMED_COLORS[name] not in allowed:
                    errs.append(f"{rel}:{ln} named color '{name}' is not a brand color")
            for m in re.finditer(r"font-family\s*:\s*([^;}\"]*(?:\"[^\"]*\"[^;}]*)*)", line):
                for fam in m.group(1).split(","):
                    fam = fam.strip().strip("'\"").lower()
                    if not fam or fam.startswith("var("):
                        continue
                    if fam not in families and fam not in GENERIC_FAMILIES:
                        errs.append(f"{rel}:{ln} font '{fam}' is not a brand font")
            for m in re.finditer(r"(?:src|href)=\"([^\"]+\.(?:svg|png|jpe?g|webp))\"", line):
                src = m.group(1)
                if "logo" in src.lower():
                    if src not in lock["logos"]:
                        errs.append(f"{rel}:{ln} logo {src} is not from brand/logos")
                    elif sha(proj / src) != lock["logos"][src]:
                        errs.append(f"{rel}:{ln} logo {src} was modified after install")
    index = (proj / "index.html").read_text() if (proj / "index.html").exists() else ""
    for el, why in (("brand-end-card", "end card"), ("brand-logo-bug", "logo bug")):
        if f'id="{el}"' not in index:
            warns.append(f"index.html has no #{el} ({why}); fine only if intentionally omitted")
    if 'href="brand/brand.css"' not in index:
        errs.append("index.html does not load brand/brand.css (fonts and tokens would be missing)")
    for w in warns:
        print(f"warn: {w}")
    for e in errs:
        print(f"FAIL: {e}")
    print(f"{'FAIL' if errs else 'PASS'}: brand lint, {len(files)} files, {len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs else 0)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("config")
    i = sub.add_parser("install"); i.add_argument("config"); i.add_argument("project")
    m = sub.add_parser("compose")
    m.add_argument("project")
    m.add_argument("--video", required=True, help="the cut (edit.py render output)")
    m.add_argument("--transcript", help="transcript.cut.json from edit.py plan")
    m.add_argument("--name", help="lower third name; omit for no lower third")
    m.add_argument("--title", help="lower third title line")
    m.add_argument("--cta", help="end card button text (default: config)")
    m.add_argument("--url", help="end card URL (default: config)")
    m.add_argument("--no-captions", action="store_true")
    m.add_argument("--caption-region", help="horizontal band for captions as fractions, e.g. 0,0.66 "
                   "keeps them left of a bottom-right facecam")
    m.add_argument("--logo-variant", default="auto", choices=["auto", "config", "on-dark", "on-light"],
                   help="auto picks the variant with contrast against the footage under the bug")
    m.add_argument("--no-end-card", action="store_true")
    l = sub.add_parser("lint"); l.add_argument("project")
    args = p.parse_args()
    if args.cmd == "compose" and not args.no_captions and not args.transcript:
        p.error("compose needs --transcript (or --no-captions)")
    {"check": cmd_check, "install": cmd_install, "compose": cmd_compose, "lint": cmd_lint}[args.cmd](args)


if __name__ == "__main__":
    main()
