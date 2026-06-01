#!/usr/bin/env python3
"""Build an organized, navigable version of the Business Extra Notes PDF.

Keeps every original page (text + images) untouched, then prepends a fancy
clickable cover + Table of Contents and adds a full hierarchical bookmark
outline so any chapter / section / week / lecture is one click away.
"""
import re
import fitz  # PyMuPDF

SRC = "Business Extra Notes 2  2 2.pdf"
OUT = "Business Extra Notes 2 - Organized.pdf"

# ----------------------------------------------------------------------------
# Palette & layout constants
# ----------------------------------------------------------------------------
NAVY   = (0.12, 0.20, 0.36)   # deep navy
NAVY2  = (0.16, 0.28, 0.48)
TEAL   = (0.16, 0.55, 0.55)
AMBER  = (0.85, 0.55, 0.13)
GRAY   = (0.42, 0.45, 0.50)
LGRAY  = (0.74, 0.76, 0.80)
INK    = (0.13, 0.15, 0.18)
WHITE  = (1, 1, 1)
TINTA  = (0.93, 0.95, 0.98)   # part A tint
TINTB  = (0.93, 0.97, 0.96)   # part B tint
TINTC  = (0.98, 0.96, 0.92)   # part C tint

PW, PH = 612.0, 792.0
ML, MR = 56.0, 56.0
MTOP, MBOT = 78.0, 60.0
USABLE_R = PW - MR

F_REG = "helv"
F_BLD = "hebo"
F_OBL = "heit"   # Helvetica oblique

PART_COLORS = {
    "A": (TEAL,  TINTA),
    "B": (NAVY2, TINTB),
    "C": (AMBER, TINTC),
}

# ----------------------------------------------------------------------------
# 1. Extract structure from the source document
# ----------------------------------------------------------------------------
chap_re = re.compile(r"^Ch\s*(\d+)\s*/?\s*(.+)", re.I)
sec_re  = re.compile(r"^(\d+)\.(\d+)\s+(.+)")
wk_re   = re.compile(r"^Week\s+(\d+)\b(.*)", re.I)
lec_re  = re.compile(r"^Lecture\s+(\d+)\b(.*)", re.I)


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip(" .\u2192-")


def first_lines(page):
    return [l.strip() for l in page.get_text().split("\n")]


def subtitle_after(lines, idx):
    junk = re.compile(r"^[-o\u2022\u25aa\d.\s]*$")
    out = []
    for l in lines[idx + 1:]:
        if l and not junk.match(l):
            out.append(l)
        if len(out) >= 1:
            break
    return clean(" ".join(out))[:78]


def extract(doc):
    n = doc.page_count
    # locate region boundaries
    week_start = lec_start = n
    for i in range(n):
        for l in first_lines(doc[i]):
            if wk_re.match(l):
                week_start = min(week_start, i)
            if lec_re.match(l):
                lec_start = min(lec_start, i)

    chapters, seen_ch, seen_sec = [], set(), set()
    cur = None
    for i in range(week_start):
        for l in first_lines(doc[i]):
            mc = chap_re.match(l)
            ms = sec_re.match(l)
            if mc:
                num = mc.group(1)
                if num in seen_ch:
                    # already have this chapter -> keep first
                    cur = next(c for c in chapters if c["num"] == num)
                    continue
                seen_ch.add(num)
                cur = {"num": num, "title": clean(mc.group(2)), "page": i, "sections": []}
                chapters.append(cur)
            elif ms:
                key = (ms.group(1), ms.group(2))
                if key in seen_sec:
                    continue
                seen_sec.add(key)
                sec = {"num": f"{ms.group(1)}.{ms.group(2)}",
                       "title": clean(ms.group(3)), "page": i,
                       "major": ms.group(1)}
                # attach to chapter whose number matches major, else current
                host = next((c for c in chapters if c["num"] == ms.group(1)), cur)
                if host is not None:
                    host["sections"].append(sec)
    chapters.sort(key=lambda c: c["page"])

    weeks = []
    for i in range(week_start, lec_start):
        lines = first_lines(doc[i])
        for j, l in enumerate(lines):
            m = wk_re.match(l)
            if m and not any(w["num"] == m.group(1) for w in weeks):
                sub = clean(m.group(2)) or subtitle_after(lines, j)
                weeks.append({"num": m.group(1), "sub": sub[:78], "page": i})

    lectures = []
    for i in range(lec_start, n):
        lines = first_lines(doc[i])
        for j, l in enumerate(lines):
            m = lec_re.match(l)
            if m and not any(x["num"] == m.group(1) for x in lectures):
                sub = clean(m.group(2)) or subtitle_after(lines, j)
                lectures.append({"num": m.group(1), "sub": sub[:78], "page": i})

    return {
        "n": n,
        "week_start": week_start,
        "lec_start": lec_start,
        "chapters": chapters,
        "weeks": weeks,
        "lectures": lectures,
    }


# ----------------------------------------------------------------------------
# 2. Build a flat list of TOC entries, then paginate
# ----------------------------------------------------------------------------
def build_entries(st):
    e = []
    # Part A
    a_end = st["week_start"]            # original 0-based exclusive
    e.append(dict(t="part", key="A", title="Chapter Notes",
                  desc="Condensed theory by chapter", page=st["chapters"][0]["page"],
                  rng=(0, a_end - 1)))
    for c in st["chapters"]:
        e.append(dict(t="chap", num=c["num"], title=c["title"], page=c["page"]))
        for s in c["sections"]:
            e.append(dict(t="sec", num=s["num"], title=s["title"], page=s["page"]))
    # Part B
    e.append(dict(t="part", key="B", title="Weekly Notes",
                  desc="Lecture-by-lecture weekly summaries", page=st["week_start"],
                  rng=(st["week_start"], st["lec_start"] - 1)))
    for w in st["weeks"]:
        e.append(dict(t="big", key="B", num=w["num"], label="Week",
                      title=f"Week {w['num']}", sub=w["sub"], page=w["page"]))
    # Part C
    e.append(dict(t="part", key="C", title="Lecture Notes",
                  desc="Detailed written lecture notes", page=st["lec_start"],
                  rng=(st["lec_start"], st["n"] - 1)))
    for l in st["lectures"]:
        e.append(dict(t="big", key="C", num=l["num"], label="Lecture",
                      title=f"Lecture {l['num']}", sub=l["sub"], page=l["page"]))
    return e


H = {"part": 52, "chap": 23, "sec": 15.5, "big": 33}


def paginate(entries):
    """Return list of pages; each page is a list of (entry, y_top)."""
    pages, cur = [], []
    y = MTOP + 30  # space for page header band
    for ent in entries:
        h = H[ent["t"]]
        # keep a part header with at least one child on the same page
        need = h + (H["chap"] if ent["t"] == "part" else 0) + 6
        if y + need > PH - MBOT:
            pages.append(cur)
            cur = []
            y = MTOP + 30
        cur.append((ent, y))
        y += h
    if cur:
        pages.append(cur)
    return pages


# ----------------------------------------------------------------------------
# 3. Rendering helpers
# ----------------------------------------------------------------------------
def text_w(s, font, size):
    return fitz.get_text_length(s, fontname=font, fontsize=size)


def fit(s, font, size, maxw):
    if text_w(s, font, size) <= maxw:
        return s
    while s and text_w(s + "\u2026", font, size) > maxw:
        s = s[:-1]
    return s + "\u2026"


def leader(shape, x0, x1, y):
    if x1 - x0 < 8:
        return
    shape.draw_line(fitz.Point(x0, y), fitz.Point(x1, y))
    shape.finish(width=0.6, color=LGRAY, dashes="[0.5 2.5] 0")


def draw_cover(page, st, offset):
    sh = page.new_shape()
    # top band
    sh.draw_rect(fitz.Rect(0, 0, PW, 196))
    sh.finish(fill=NAVY, color=NAVY)
    sh.draw_rect(fitz.Rect(0, 196, PW, 202))
    sh.finish(fill=TEAL, color=TEAL)
    sh.commit()

    page.insert_text((ML, 92), "BUSINESS", fontname=F_BLD, fontsize=15, color=(0.6, 0.78, 0.85))
    page.insert_text((ML, 132), "Markets & Organizations", fontname=F_BLD, fontsize=30, color=WHITE)
    page.insert_text((ML, 166), "Complete Study Notes \u00b7 organized & navigable",
                     fontname=F_REG, fontsize=13, color=(0.80, 0.85, 0.92))

    page.insert_text((ML, 246), "Jump to any part \u2014 click a card or open the Contents that follow.",
                     fontname=F_REG, fontsize=11.5, color=GRAY)

    cards = [
        ("A", "Chapter Notes", st["chapters"][0]["page"],
         f"{len(st['chapters'])} chapters \u00b7 condensed theory"),
        ("B", "Weekly Notes", st["week_start"],
         f"{len(st['weeks'])} weeks \u00b7 weekly summaries"),
        ("C", "Lecture Notes", st["lec_start"],
         f"{len(st['lectures'])} lectures \u00b7 detailed notes"),
    ]
    y = 280
    for key, title, opage, desc in cards:
        accent, tint = PART_COLORS[key]
        r = fitz.Rect(ML, y, USABLE_R, y + 86)
        sh = page.new_shape()
        sh.draw_rect(r); sh.finish(fill=tint, color=tint)
        sh.draw_rect(fitz.Rect(r.x0, r.y0, r.x0 + 8, r.y1)); sh.finish(fill=accent, color=accent)
        sh.commit()
        page.insert_text((r.x0 + 26, y + 38), f"PART {key}", fontname=F_BLD, fontsize=13, color=accent)
        page.insert_text((r.x0 + 26, y + 62), title, fontname=F_BLD, fontsize=20, color=INK)
        page.insert_text((r.x0 + 200, y + 62), desc, fontname=F_REG, fontsize=11, color=GRAY)
        newp = opage + offset + 1
        pn = f"p. {newp}"
        page.insert_text((USABLE_R - 24 - text_w(pn, F_BLD, 13), y + 38),
                         pn, fontname=F_BLD, fontsize=13, color=accent)
        page.insert_link({"kind": fitz.LINK_GOTO, "from": r,
                          "page": opage + offset, "to": fitz.Point(0, 0)})
        y += 102

    page.insert_text((ML, PH - 40),
                     f"{st['n']} pages \u00b7 every diagram and image preserved",
                     fontname=F_OBL, fontsize=10, color=GRAY)


def draw_toc_header(page, idx, total):
    sh = page.new_shape()
    sh.draw_rect(fitz.Rect(0, 0, PW, 50)); sh.finish(fill=NAVY, color=NAVY)
    sh.draw_rect(fitz.Rect(0, 50, PW, 52.5)); sh.finish(fill=TEAL, color=TEAL)
    sh.commit()
    page.insert_text((ML, 33), "CONTENTS", fontname=F_BLD, fontsize=15, color=WHITE)
    lbl = f"Table of Contents  \u00b7  {idx}/{total}"
    page.insert_text((USABLE_R - text_w(lbl, F_REG, 10), 32), lbl,
                     fontname=F_REG, fontsize=10, color=(0.75, 0.82, 0.90))


def draw_entry(page, ent, y, offset):
    newp = ent["page"] + offset + 1
    pn = str(newp)
    if ent["t"] == "part":
        accent, tint = PART_COLORS[ent["key"]]
        r = fitz.Rect(ML, y + 8, USABLE_R, y + 46)
        sh = page.new_shape()
        sh.draw_rect(r); sh.finish(fill=tint, color=tint)
        sh.draw_rect(fitz.Rect(r.x0, r.y0, r.x0 + 6, r.y1)); sh.finish(fill=accent, color=accent)
        sh.commit()
        page.insert_text((ML + 18, y + 26), f"PART {ent['key']}", fontname=F_BLD, fontsize=11, color=accent)
        page.insert_text((ML + 18, y + 42), ent["title"], fontname=F_BLD, fontsize=15, color=INK)
        page.insert_text((ML + 200, y + 42), ent["desc"], fontname=F_REG, fontsize=9.5, color=GRAY)
        rng = f"pp. {ent['rng'][0] + offset + 1}\u2013{ent['rng'][1] + offset + 1}"
        page.insert_text((USABLE_R - 14 - text_w(rng, F_BLD, 11), y + 30),
                         rng, fontname=F_BLD, fontsize=11, color=accent)
        link_rect = r
        target_y = 0

    elif ent["t"] == "chap":
        badge = fitz.Rect(ML, y + 2, ML + 34, y + 19)
        sh = page.new_shape(); sh.draw_rect(badge); sh.finish(fill=NAVY, color=NAVY); sh.commit()
        page.insert_text((badge.x0 + 5, y + 14.5), f"Ch{ent['num']}", fontname=F_BLD, fontsize=8.5, color=WHITE)
        tx = ML + 44
        title = fit(ent["title"], F_BLD, 11.5, 360)
        page.insert_text((tx, y + 15), title, fontname=F_BLD, fontsize=11.5, color=INK)
        tw = text_w(title, F_BLD, 11.5)
        page.insert_text((USABLE_R - text_w(pn, F_BLD, 11), y + 15), pn, fontname=F_BLD, fontsize=11, color=TEAL)
        sh = page.new_shape()
        leader(sh, tx + tw + 8, USABLE_R - text_w(pn, F_BLD, 11) - 8, y + 12)
        sh.commit()
        link_rect = fitz.Rect(ML, y, USABLE_R, y + H["chap"])
        target_y = 0

    elif ent["t"] == "sec":
        tx = ML + 52
        page.insert_text((tx - 14, y + 11), "\u2022", fontname=F_BLD, fontsize=10, color=LGRAY)
        label = f"{ent['num']}  {ent['title']}"
        label = fit(label, F_REG, 10, 360)
        page.insert_text((tx, y + 11), label, fontname=F_REG, fontsize=10, color=(0.28, 0.30, 0.34))
        tw = text_w(label, F_REG, 10)
        page.insert_text((USABLE_R - text_w(pn, F_REG, 10), y + 11), pn, fontname=F_REG, fontsize=10, color=GRAY)
        sh = page.new_shape()
        leader(sh, tx + tw + 8, USABLE_R - text_w(pn, F_REG, 10) - 8, y + 9)
        sh.commit()
        link_rect = fitz.Rect(ML, y, USABLE_R, y + H["sec"])
        target_y = 0

    else:  # big (week / lecture)
        accent, tint = PART_COLORS[ent["key"]]
        badge = fitz.Rect(ML, y + 3, ML + 30, y + 27)
        sh = page.new_shape(); sh.draw_rect(badge); sh.finish(fill=accent, color=accent); sh.commit()
        page.insert_text((badge.x0 + 9, y + 20), ent["num"], fontname=F_BLD, fontsize=12, color=WHITE)
        tx = ML + 42
        page.insert_text((tx, y + 14), ent["title"], fontname=F_BLD, fontsize=12, color=INK)
        if ent["sub"]:
            page.insert_text((tx, y + 28), fit(ent["sub"], F_OBL, 9.5, 380),
                             fontname=F_OBL, fontsize=9.5, color=GRAY)
        page.insert_text((USABLE_R - text_w(pn, F_BLD, 11.5), y + 14), pn, fontname=F_BLD, fontsize=11.5, color=accent)
        link_rect = fitz.Rect(ML, y, USABLE_R, y + H["big"])
        target_y = 0

    page.insert_link({"kind": fitz.LINK_GOTO, "from": link_rect,
                      "page": ent["page"] + offset, "to": fitz.Point(0, target_y)})


# ----------------------------------------------------------------------------
# 4. Bookmark outline
# ----------------------------------------------------------------------------
def build_toc_outline(st, offset):
    toc = []
    toc.append([1, "Part A \u2014 Chapter Notes", st["chapters"][0]["page"] + offset + 1])
    for c in st["chapters"]:
        toc.append([2, f"Ch{c['num']} \u2014 {c['title']}", c["page"] + offset + 1])
        for s in c["sections"]:
            toc.append([3, f"{s['num']} {s['title']}", s["page"] + offset + 1])
    toc.append([1, "Part B \u2014 Weekly Notes", st["week_start"] + offset + 1])
    for w in st["weeks"]:
        t = f"Week {w['num']}" + (f" \u2014 {w['sub']}" if w["sub"] else "")
        toc.append([2, t, w["page"] + offset + 1])
    toc.append([1, "Part C \u2014 Lecture Notes", st["lec_start"] + offset + 1])
    for l in st["lectures"]:
        t = f"Lecture {l['num']}" + (f" \u2014 {l['sub']}" if l["sub"] else "")
        toc.append([2, t, l["page"] + offset + 1])
    return toc


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    src = fitz.open(SRC)
    st = extract(src)
    entries = build_entries(st)
    toc_pages = paginate(entries)
    offset = 1 + len(toc_pages)            # cover + toc pages

    out = fitz.open()
    # create front matter pages
    for _ in range(offset):
        out.new_page(width=PW, height=PH)
    # append original content
    out.insert_pdf(src)

    # draw cover
    draw_cover(out[0], st, offset)
    # draw toc pages
    total = len(toc_pages)
    for pi, items in enumerate(toc_pages):
        page = out[1 + pi]
        draw_toc_header(page, pi + 1, total)
        for ent, y in items:
            draw_entry(page, ent, y, offset)

    out.set_toc(build_toc_outline(st, offset))
    out.set_metadata({
        "title": "Business: Markets & Organizations \u2014 Study Notes",
        "author": "",
        "subject": "Organized & navigable study notes",
        "keywords": "markets, organizations, chapters, weeks, lectures",
    })
    out.save(OUT, deflate=True, garbage=3)
    print(f"Saved {OUT}: {out.page_count} pages (offset {offset}, {total} TOC pages)")
    print(f"Chapters: {len(st['chapters'])}, Weeks: {len(st['weeks'])}, Lectures: {len(st['lectures'])}")
    out.close(); src.close()


if __name__ == "__main__":
    main()
