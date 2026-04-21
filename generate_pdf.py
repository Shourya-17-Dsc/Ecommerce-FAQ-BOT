"""
E-Commerce FAQ Bot — Project Documentation PDF
Spec : A4 | Arial 15pt Heading / 14pt Subheading / 12pt Body Justified
       Page numbers bottom-right | Light clean theme | Screenshot spaces blank
Layout plan (5 pages total):
  Page 1 — Cover
  Page 2 — Problem Statement + Solution / Features + Architecture
  Page 3 — Screenshots (5 placeholders) + Tech Stack
  Page 4 — Unique Points + Future Improvements
  Page 5 — Project Summary
"""

import sys, os
sys.stdout.reconfigure(encoding="utf-8")

from reportlab.lib.pagesizes   import A4
from reportlab.lib              import colors
from reportlab.lib.units        import mm
from reportlab.lib.styles       import ParagraphStyle
from reportlab.lib.enums        import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus         import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.pdfgen           import canvas
from reportlab.pdfbase          import pdfmetrics
from reportlab.pdfbase.ttfonts  import TTFont

# ── Font registration (Windows Arial) ────────────────────────────────────────
_FD = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Ar",  os.path.join(_FD, "arial.ttf")))
pdfmetrics.registerFont(TTFont("ArB", os.path.join(_FD, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("ArI", os.path.join(_FD, "ariali.ttf")))
pdfmetrics.registerFontFamily("Ar", normal="Ar", bold="ArB", italic="ArI")

# ── Colour palette (light monotone) ──────────────────────────────────────────
C = {
    "text":    colors.HexColor("#111111"),       # body text
    "head":    colors.HexColor("#1C2B3A"),       # headings
    "acc":     colors.HexColor("#2E5FA3"),       # accent blue
    "rule":    colors.HexColor("#C5CDD6"),       # table borders / rules
    "sbg":     colors.HexColor("#EEF2F7"),       # section bar bg
    "trhdr":   colors.HexColor("#2E5FA3"),       # table header bg
    "trod":    colors.white,
    "trev":    colors.HexColor("#F0F4F9"),
    "ibg":     colors.HexColor("#EBF0F8"),       # info-box bg
    "scrbg":   colors.HexColor("#F5F7FA"),       # screenshot placeholder
    "scrbdr":  colors.HexColor("#AAB8C2"),       # screenshot border
    "scrtxt":  colors.HexColor("#7F96A8"),       # screenshot label colour
    "subtle":  colors.HexColor("#5A6A78"),       # captions / footer
    "white":   colors.white,
    "cvdk":    colors.HexColor("#1C2B3A"),       # cover dark zone
}

# A4 page: 210 mm wide; margins 18 mm each side → usable width = 174 mm
# A4 page: 297 mm tall;  margins top=22 mm, bottom=18 mm → usable height = 257 mm
CW  = A4[0] - 36 * mm      # 174 mm
PH  = 257 * mm              # usable page height (for reference)


# ── Paragraph style factory ───────────────────────────────────────────────────
def _p(nm, fn="Ar", sz=12, col=None, al=TA_JUSTIFY, ld=None, sb=0, sa=3, li=0):
    col = col or C["text"]
    ld  = ld  or int(sz * 1.42)
    return ParagraphStyle(nm, fontName=fn, fontSize=sz, textColor=col,
                          alignment=al, leading=ld,
                          spaceBefore=sb, spaceAfter=sa, leftIndent=li)

# Heading/body styles (per spec: H1=15pt, H2=14pt, body=12pt)
ST = {
    "H1":  _p("H1",  fn="ArB", sz=15, col=C["head"], al=TA_LEFT,  ld=20, sb=6,  sa=3),
    "H2":  _p("H2",  fn="ArB", sz=14, col=C["acc"],  al=TA_LEFT,  ld=18, sb=4,  sa=2),
    "H3":  _p("H3",  fn="ArB", sz=12, col=C["head"], al=TA_LEFT,  ld=16, sb=3,  sa=1),
    "BD":  _p("BD",  sz=12,          col=C["text"], al=TA_JUSTIFY,ld=18, sb=0,  sa=3),
    "CP":  _p("CP",  fn="ArI", sz=9,  col=C["subtle"],al=TA_CENTER,ld=12, sb=1,  sa=3),
    # table
    "TH":  _p("TH",  fn="ArB", sz=10, col=C["white"], al=TA_CENTER,ld=13, sb=0,  sa=0),
    "TC":  _p("TC",  sz=9,           col=C["text"],  al=TA_LEFT,  ld=12, sb=0,  sa=0),
    "TCC": _p("TCC", sz=9,           col=C["text"],  al=TA_CENTER,ld=12, sb=0,  sa=0),
    "TCB": _p("TCB", fn="ArB", sz=9,  col=C["head"],  al=TA_LEFT,  ld=12, sb=0,  sa=0),
    # screenshot labels
    "SL":  _p("SL",  fn="ArB", sz=10, col=C["scrtxt"],al=TA_CENTER,ld=14, sb=0,  sa=2),
    "SS":  _p("SS",  fn="ArI", sz=8,  col=C["scrtxt"],al=TA_CENTER,ld=11, sb=0,  sa=0),
}
SP = Spacer


# ── Table helper (standard styled table) ─────────────────────────────────────
def tbl(data, widths, c0_centre=True):
    rows = []
    for ri, row in enumerate(data):
        r = []
        for ci, cell in enumerate(row):
            if not isinstance(cell, str):
                r.append(cell); continue
            if ri == 0:
                r.append(Paragraph(cell, ST["TH"]))
            elif ci == 0:
                r.append(Paragraph(cell, ST["TCC"] if c0_centre else ST["TCB"]))
            else:
                r.append(Paragraph(cell, ST["TC"]))
        rows.append(r)
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  C["trhdr"]),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [C["trod"],C["trev"]]),
        ("BOX",           (0,0),(-1,-1), 0.6, C["rule"]),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, C["rule"]),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("ALIGN",         (0,1),(0,-1),  "CENTRE"),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("RIGHTPADDING",  (0,0),(-1,-1), 5),
    ]))
    return t


# ── Section heading bar (H1 15pt, blue-left-border) ───────────────────────────
def sec(num, title):
    t = Table([[Paragraph(f"{num}.&nbsp; {title}", ST["H1"])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), C["sbg"]),
        ("LINEBEFORE",    (0,0),(0,-1),  5, C["acc"]),
        ("LINEBELOW",     (0,0),(-1,-1), 0.5, C["rule"]),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
    ]))
    return t


# ── Info box ──────────────────────────────────────────────────────────────────
def ibox(text):
    t = Table([[Paragraph(text, ST["BD"])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), C["ibg"]),
        ("LINEBEFORE",   (0,0),(0,-1),  4, C["acc"]),
        ("BOX",          (0,0),(-1,-1), 0.5, C["rule"]),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ]))
    return t


# ── Screenshot placeholder (full-width) ───────────────────────────────────────
def scr(title, note, h=38*mm):
    inner = Table(
        [[Paragraph(title, ST["SL"])],
         [Paragraph(note,  ST["SS"])]],
        colWidths=[CW - 6*mm]
    )
    inner.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
        ("ALIGN",        (0,0),(-1,-1),"CENTRE"),
        ("TOPPADDING",   (0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
    ]))
    outer = Table([[inner]], colWidths=[CW], rowHeights=[h])
    outer.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), C["scrbg"]),
        ("BOX",          (0,0),(-1,-1), 1.0, C["scrbdr"]),
        ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
        ("ALIGN",        (0,0),(-1,-1),"CENTRE"),
        ("TOPPADDING",   (0,0),(-1,-1),3),
        ("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING",  (0,0),(-1,-1),3),
        ("RIGHTPADDING", (0,0),(-1,-1),3),
    ]))
    return outer


# ── Two screenshot placeholders side-by-side ──────────────────────────────────
def scr2(items, h=34*mm):
    hw = (CW - 3*mm) / 2     # half width ≈ 85.5 mm
    cells = []
    for title, note in items:
        inner = Table(
            [[Paragraph(title, ST["SL"])],
             [Paragraph(note,  ST["SS"])]],
            colWidths=[hw - 5*mm]
        )
        inner.setStyle(TableStyle([
            ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
            ("ALIGN",        (0,0),(-1,-1),"CENTRE"),
            ("TOPPADDING",   (0,0),(-1,-1),0),
            ("BOTTOMPADDING",(0,0),(-1,-1),0),
            ("LEFTPADDING",  (0,0),(-1,-1),2),
            ("RIGHTPADDING", (0,0),(-1,-1),2),
        ]))
        box = Table([[inner]], colWidths=[hw], rowHeights=[h])
        box.setStyle(TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), C["scrbg"]),
            ("BOX",          (0,0),(-1,-1), 1.0, C["scrbdr"]),
            ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
            ("ALIGN",        (0,0),(-1,-1),"CENTRE"),
            ("TOPPADDING",   (0,0),(-1,-1),3),
            ("BOTTOMPADDING",(0,0),(-1,-1),3),
            ("LEFTPADDING",  (0,0),(-1,-1),2),
            ("RIGHTPADDING", (0,0),(-1,-1),2),
        ]))
        cells.append(box)
    outer = Table([cells], colWidths=[hw, hw])
    outer.setStyle(TableStyle([
        ("LEFTPADDING", (0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",  (0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("VALIGN",      (0,0),(-1,-1),"TOP"),
    ]))
    return outer


# ── Page decorators ───────────────────────────────────────────────────────────
def cover(canv, doc):
    W, H = A4
    # Dark top zone (top 54%)
    canv.setFillColor(C["cvdk"])
    canv.rect(0, H*0.46, W, H*0.54, fill=1, stroke=0)
    # Accent divider stripe
    canv.setFillColor(C["acc"])
    canv.rect(0, H*0.46 - 2.5*mm, W, 2.5*mm, fill=1, stroke=0)
    # Light bottom zone
    canv.setFillColor(colors.HexColor("#F6F8FB"))
    canv.rect(0, 0, W, H*0.46 - 2.5*mm, fill=1, stroke=0)
    # Top bar
    canv.setFillColor(C["acc"])
    canv.rect(0, H-5*mm, W, 5*mm, fill=1, stroke=0)
    # Bottom bar
    canv.setFillColor(C["cvdk"])
    canv.rect(0, 0, W, 7*mm, fill=1, stroke=0)

    # Circle icon
    canv.setFillColor(C["acc"])
    canv.circle(W/2, H*0.73, 20*mm, fill=1, stroke=0)
    canv.setFillColor(C["white"])
    canv.setFont("ArB", 12)
    canv.drawCentredString(W/2, H*0.73 - 2*mm, "FAQ BOT")

    # Title
    canv.setFont("ArB", 26)
    canv.setFillColor(C["white"])
    canv.drawCentredString(W/2, H*0.73 - 22*mm, "E-Commerce FAQ Bot")

    # Subtitle
    canv.setFont("Ar", 12)
    canv.setFillColor(colors.HexColor("#A8C0D8"))
    canv.drawCentredString(W/2, H*0.73 - 33*mm,
                           "ShopEasy AI-Powered Customer Support Agent")

    # Horizontal rule
    canv.setStrokeColor(C["acc"])
    canv.setLineWidth(0.8)
    canv.line(35*mm, H*0.73 - 40*mm, W-35*mm, H*0.73 - 40*mm)

    # Tech tags
    canv.setFont("Ar", 9.5)
    canv.setFillColor(colors.HexColor("#7A9BB8"))
    canv.drawCentredString(W/2, H*0.73 - 49*mm,
                           "LangGraph  ·  ChromaDB  ·  Groq LLaMA-3.3-70B  ·  Streamlit")

    # Info block in light zone
    rows = [
        ("DOCUMENT TYPE",  "Project Documentation"),
        ("DOMAIN",         "E-Commerce Customer Support"),
        ("FRAMEWORK",      "LangGraph + ChromaDB (Agentic AI)"),
        ("LLM MODEL",      "Groq — LLaMA-3.3-70B-Versatile"),
        ("COURSE / YEAR",  "Agentic AI Capstone — 2026"),
    ]
    by = H*0.46 - 24*mm
    for i, (lbl, val) in enumerate(rows):
        y = by - i * 13*mm
        canv.setFont("ArB", 7.5); canv.setFillColor(C["subtle"])
        canv.drawString(28*mm, y + 3.5*mm, lbl)
        canv.setFont("Ar", 11);   canv.setFillColor(C["text"])
        canv.drawString(28*mm, y - 3.5*mm, val)
        if i < len(rows)-1:
            canv.setStrokeColor(C["rule"]); canv.setLineWidth(0.3)
            canv.line(28*mm, y-7*mm, W-28*mm, y-7*mm)

    # Footer
    canv.setFont("Ar", 7.5)
    canv.setFillColor(colors.HexColor("#6A7F90"))
    canv.drawCentredString(W/2, 2*mm,
        "Dr. Kanthi Kiran Sirra  ·  Agentic AI Capstone 2026  ·  Confidential")


def inner_page(canv, doc):
    W, H = A4
    # Header bar
    canv.setFillColor(C["cvdk"])
    canv.rect(0, H-17*mm, W, 17*mm, fill=1, stroke=0)
    canv.setFillColor(C["acc"])
    canv.rect(0, H-18.5*mm, W, 1.5*mm, fill=1, stroke=0)
    canv.setFont("ArB", 8.5); canv.setFillColor(C["white"])
    canv.drawString(18*mm, H-10*mm, "E-Commerce FAQ Bot  —  Project Documentation")
    canv.setFont("Ar", 8); canv.setFillColor(colors.HexColor("#A8BDD8"))
    canv.drawRightString(W-18*mm, H-10*mm, "ShopEasy AI Support")
    # Footer rule
    canv.setStrokeColor(C["rule"]); canv.setLineWidth(0.5)
    canv.line(18*mm, 14*mm, W-18*mm, 14*mm)
    canv.setFont("Ar", 7.5); canv.setFillColor(C["subtle"])
    canv.drawString(18*mm, 7.5*mm, "Agentic AI Capstone Project  ·  2026")
    # Page number bottom-right
    canv.setFont("ArB", 9); canv.setFillColor(C["head"])
    canv.drawRightString(W-18*mm, 7.5*mm, f"Page  {doc.page}")


# ── Document story ────────────────────────────────────────────────────────────
def build():
    fl = []

    # ════════════════════════════════════════════════════════════
    # PAGE 2  —  Problem Statement  +  Solution  +  Architecture
    # Budget ≈ 257 mm  |  Estimated use ≈ 248 mm
    # ════════════════════════════════════════════════════════════

    # 1. Problem Statement
    fl += [sec("1","Problem Statement"), SP(1,4)]
    fl.append(Paragraph(
        "Modern e-commerce platforms receive millions of repetitive customer queries "
        "daily — returns, order status, payments, shipping, coupons, and warranties. "
        "Handling these through human agents is costly, slow, and unscalable. "
        "Traditional rule-based chatbots are rigid and cannot retrieve grounded answers "
        "from dynamic policies. An intelligent, always-available agent that understands "
        "intent, retrieves accurate information, and evaluates its own answers is needed.",
        ST["BD"]))

    # 2. Solution / Features
    fl += [SP(1,3), sec("2","Solution / Features"), SP(1,4)]
    fl.append(ibox(
        "<b>ShopEasy AI FAQ Bot</b> is an Agentic AI system built with LangGraph, "
        "ChromaDB-backed semantic RAG, Groq LLaMA-3.3-70B, and a self-reflection "
        "faithfulness evaluation loop — delivering accurate 24×7 customer support "
        "with zero human intervention."))
    fl += [SP(1,4)]

    # Features table — descriptions kept to 1 line (≤ 75 chars in 136 mm column)
    fl.append(tbl([
        ["Feature",               "Description"],
        ["Intelligent Routing",   "LLM routes each query to KB retrieve, real-time tool, or skip."],
        ["Semantic RAG",          "12 docs embedded via SentenceTransformer; top-3 fetched from ChromaDB."],
        ["Self-Reflection Eval",  "Answer scored 0.0–1.0 for faithfulness; auto-retry if < 0.7 (max 2×)."],
        ["Real-Time Tools",       "Order tracker, discount calculator, datetime, and support contact."],
        ["Persistent Memory",     "MemorySaver + 6-msg window retains name, order ID, and context."],
        ["Premium Streamlit UI",  "Dark glassmorphism chat with per-response route/faith/source badges."],
    ], [38*mm, CW-38*mm]))

    # 3. System Architecture
    fl += [SP(1,5), sec("3","System Architecture &amp; Graph Flow"), SP(1,4)]
    fl.append(Paragraph(
        "The bot is a <b>LangGraph StateGraph</b> of eight nodes sharing "
        "<i>CapstoneState</i>. Two conditional edges decide execution path: "
        "<i>route_decision</i> (retrieve | tool | skip) and "
        "<i>eval_decision</i> (retry if faithfulness &lt; 0.7, else save).",
        ST["BD"]))
    fl += [SP(1,4)]

    # Nodes table — descriptions ≤ 70 chars in 150 mm column
    fl.append(tbl([
        ["Node",      "Responsibility"],
        ["memory",    "Append message to 6-msg window; extract name and order ID via regex."],
        ["router",    "LLM classifies query: retrieve | tool | skip."],
        ["retrieve",  "Encode query with SentenceTransformer; fetch top-3 ChromaDB chunks."],
        ["skip",      "Pass empty context for greetings — bypasses ChromaDB entirely."],
        ["tool",      "Dispatch to order tracker / price calc / datetime / support contact."],
        ["answer",    "Call Groq LLaMA-3.3-70B with KB context + history; generate reply."],
        ["eval",      "Score faithfulness 0.0–1.0; route back to answer if score < 0.7."],
        ["save",      "Append reply to messages; MemorySaver writes state checkpoint."],
    ], [24*mm, CW-24*mm]))
    fl.append(Paragraph(
        "Table 1 — 8-node flow: START → memory → router → [retrieve|skip|tool] "
        "→ answer → eval → [retry | save] → END",
        ST["CP"]))

    fl.append(PageBreak())

    # ════════════════════════════════════════════════════════════
    # PAGE 3  —  Screenshots (5)  +  Tech Stack
    # Budget ≈ 257 mm  |  Estimated use ≈ 248 mm
    # ════════════════════════════════════════════════════════════

    fl += [sec("4","Application Screenshots"), SP(1,4)]
    fl.append(Paragraph(
        "Five screenshots below show key views of the ShopEasy AI FAQ Bot. "
        "Space is left blank — attach actual screenshots before submission.",
        ST["BD"]))
    fl += [SP(1,4)]

    fl.append(scr(
        "Screenshot 1  —  Main Chat Interface",
        "[ Insert screenshot here: full chat window showing the dark-themed UI, "
        "glassmorphism bot bubble, orange user bubble, and meta-badge strip ]",
        h=40*mm))
    fl.append(Paragraph(
        "Figure 1 — Main chat view with glassmorphism bot bubble (left), "
        "orange user bubble (right), and meta-badge strip (route · faithfulness · KB sources).",
        ST["CP"]))
    fl += [SP(1,3)]

    fl.append(scr2([
        ("Screenshot 2  —  Sidebar Panel",
         "[ Insert screenshot: sidebar showing brand, topic pills, "
         "quick-question buttons, session stats ]"),
        ("Screenshot 3  —  Welcome / Empty State",
         "[ Insert screenshot: welcome card on fresh session "
         "with four quick-chip suggestion buttons ]"),
    ], h=36*mm))
    fl.append(Paragraph(
        "Figure 2 (left) — Sidebar navigation panel with topic pills and quick-question shortcuts.   "
        "Figure 3 (right) — Welcome screen shown at the start of a new session.",
        ST["CP"]))
    fl += [SP(1,3)]

    fl.append(scr2([
        ("Screenshot 4  —  Order Tracking Response",
         "[ Insert screenshot: tool-route response for order query "
         "with status, ETA, and route=Tool badge ]"),
        ("Screenshot 5  —  Self-Reflection Retry",
         "[ Insert screenshot: eval node triggering retry on "
         "faithfulness=0.58; regenerated reply = 0.91 ]"),
    ], h=36*mm))
    fl.append(Paragraph(
        "Figure 4 (left) — Tool-route order-tracking response with live status and ETA.   "
        "Figure 5 (right) — Self-reflection retry raising faithfulness score from 0.58 to 0.91.",
        ST["CP"]))
    fl += [SP(1,4)]

    # 5. Tech Stack  — purpose column ≤ 48 chars (≈ 82 mm column)
    fl += [sec("5","Technology Stack"), SP(1,4)]
    fl.append(tbl([
        ["Layer",               "Technology",                          "Purpose / Role"],
        ["Agentic Framework",   "LangGraph 0.2.x",                    "StateGraph, conditional edges, MemorySaver"],
        ["LLM",                 "Groq — LLaMA-3.3-70B-Versatile",     "Routing, generation, faithfulness eval"],
        ["Embeddings",          "SentenceTransformer all-MiniLM-L6-v2","384-dim bi-encoder for KB and queries"],
        ["Vector Database",     "ChromaDB in-memory (cosine)",         "Semantic search over 12 policy docs"],
        ["UI Framework",        "Streamlit 1.x",                       "Dark chat UI with bubbles and meta-badges"],
        ["REST API",            "FastAPI + Uvicorn",                   "POST /ask · GET /health · POST /reset"],
        ["Evaluation",          "RAGAS metrics",                      "Faithfulness, relevancy, context precision"],
        ["Language",            "Python 3.10+",                        "Package, notebook, API, tests, Streamlit"],
    ], [34*mm, 50*mm, CW-84*mm]))
    fl.append(Paragraph("Table 2 — Full technology stack.", ST["CP"]))

    fl.append(PageBreak())

    # ════════════════════════════════════════════════════════════
    # PAGE 4  —  Unique Points  +  Future Improvements
    # Budget ≈ 257 mm  |  Estimated use ≈ 244 mm
    # ════════════════════════════════════════════════════════════

    # 6. Unique Points — description column 132 mm ≈ 374pt → ~75 chars max
    fl += [sec("6","Unique Points &amp; Differentiators"), SP(1,4)]
    fl.append(tbl([
        ["Differentiator",                  "Description"],
        ["Self-Reflecting Quality Gate",    "Bot scores own faithfulness (0–1); answers < 0.7 auto-regenerated."],
        ["Three-Way Intelligent Routing",   "Router selects retrieve / tool / skip per query dynamically."],
        ["Persistent Multi-Turn Memory",    "MemorySaver keeps name, order IDs, and dialogue thread across turns."],
        ["Full Transparency Metadata",      "Route, faithfulness, and KB sources shown as per-response badges."],
        ["Comprehensive 12-Document KB",    "Covers all ShopEasy topics: returns, payments, coupons, warranty…"],
        ["Lazy-Import Architecture",        "Circular import between agent.py and nodes.py resolved via lazy load."],
    ], [48*mm, CW-48*mm], c0_centre=False))
    fl += [SP(1,5)]

    # 7. Future Improvements — description column 102 mm ≈ 289pt → ~58 chars max
    fl += [sec("7","Future Improvements"), SP(1,4)]
    fl.append(tbl([
        ["Enhancement",                 "Description",                                               "Priority"],
        ["Live Order DB Integration",   "Replace mock tracker with real order management API.",       "High"],
        ["Multi-Language Support",      "Translation layer for Hindi, Telugu, Tamil, and others.",    "High"],
        ["Voice Input / Output",        "Whisper STT + TTS for voice-based mobile support.",          "Medium"],
        ["RAGAS Auto-Eval Pipeline",    "Auto-run faithfulness checks on every KB document update.",  "Medium"],
        ["Human Escalation Path",       "Detect frustration; route query to live human agent.",       "Medium"],
        ["Admin Analytics Dashboard",   "Track volume, topics, faithfulness scores, retry rates.",    "Low"],
        ["Persistent Vector Store",     "Migrate ChromaDB to Pinecone or Qdrant for production.",     "Low"],
    ], [46*mm, CW-70*mm, 24*mm]))
    fl.append(Paragraph("Table 3 — Future improvements roadmap with priority classification.",
                         ST["CP"]))

    fl.append(PageBreak())

    # ════════════════════════════════════════════════════════════
    # PAGE 5  —  Project Summary
    # Budget ≈ 257 mm  |  Estimated use ≈ 120 mm
    # ════════════════════════════════════════════════════════════

    fl += [sec("8","Project Summary"), SP(1,5)]

    sum_rows = [
        ("Project Name",    "E-Commerce FAQ Bot  —  ShopEasy AI Customer Support Agent"),
        ("Domain",          "E-Commerce Customer Support Automation"),
        ("Core Technique",  "Retrieval-Augmented Generation (RAG) + LangGraph Agentic Pipeline"),
        ("Graph Nodes",     "8 nodes — memory · router · retrieve · skip · tool · answer · eval · save"),
        ("Knowledge Base",  "12 embedded docs: returns, refunds, shipping, payments, coupons, warranty, SuperCoins"),
        ("Self-Evaluation", "LLM faithfulness scoring 0.0–1.0; auto-retry if < 0.7 (max 2 retries per turn)"),
        ("Submission Files","day13_capstone.ipynb   ·   capstone_streamlit.py   ·   agent.py"),
        ("Course",          "Agentic AI Capstone — Dr. Kanthi Kiran Sirra  ·  2026"),
    ]
    rows = []
    for lbl, val in sum_rows:
        rows.append([Paragraph(lbl, ST["TCB"]), Paragraph(val, ST["TC"])])
    sum_t = Table(rows, colWidths=[40*mm, CW-40*mm])
    sum_t.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0),(-1,-1), [C["trod"],C["trev"]]),
        ("BOX",            (0,0),(-1,-1), 0.7, C["rule"]),
        ("INNERGRID",      (0,0),(-1,-1), 0.3, C["rule"]),
        ("LINEBEFORE",     (0,0),(0,-1),  4,   C["acc"]),
        ("VALIGN",         (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",     (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING",    (0,0),(-1,-1), 6),
        ("RIGHTPADDING",   (0,0),(-1,-1), 6),
    ]))
    fl.append(sum_t)

    return fl


# ── Build & save ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    OUT = (r"C:\Users\KIIT0001\OneDrive\Desktop\Agentic ai"
           r"\AgenticAI_Capstone_EcommerceBot\E-commerce Faq bot.pdf")

    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=22*mm,     # inner_page header = 18.5 mm; 22 gives 3.5 mm buffer
        bottomMargin=18*mm,  # footer rule at 14 mm; 18 gives 4 mm buffer
        title="E-Commerce FAQ Bot — Project Documentation",
        author="Agentic AI Capstone 2026",
        subject="ShopEasy AI-Powered Customer Support Agent",
        creator="ReportLab / Python",
    )

    doc.build(build(), onFirstPage=cover, onLaterPages=inner_page)

    from pypdf import PdfReader
    r  = PdfReader(OUT)
    sz = os.path.getsize(OUT) / (1024*1024)
    print(f"\n{'='*55}")
    print(f"  File  : {os.path.basename(OUT)}")
    print(f"  Path  : {OUT}")
    print(f"  Pages : {len(r.pages)}  (requirement: 4–5)")
    print(f"  Size  : {sz:.2f} MB  (limit: 10 MB)")
    print(f"{'='*55}")
