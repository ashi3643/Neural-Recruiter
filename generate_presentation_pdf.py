#!/usr/bin/env python3
"""
Generate PDF presentation deck for Neural Recruiter
Uses reportlab to create a professional PDF with slide-like appearance
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# Create PDF with custom page setup
pdf_file = "PRESENTATION.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch,
                        leftMargin=0.75*inch, rightMargin=0.75*inch)

# Get sample styles and create custom ones
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=36,
    textColor=HexColor('#667eea'),
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=24,
    textColor=HexColor('#667eea'),
    spaceAfter=15,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=11,
    textColor=black,
    spaceAfter=12,
    alignment=TA_JUSTIFY,
    leading=16
)

bullet_style = ParagraphStyle(
    'Bullet',
    parent=styles['Normal'],
    fontSize=11,
    textColor=black,
    leftIndent=20,
    spaceAfter=8,
    leading=14
)

# Build story
story = []

# Slide 1: Title
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("🧠 Neural Recruiter", title_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Intelligent Candidate Discovery & Ranking", ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=16, alignment=TA_CENTER, textColor=HexColor('#764ba2'))))
story.append(Spacer(1, 0.4*inch))
story.append(Paragraph("Track 01 | Data & AI Challenge 2026", ParagraphStyle('sub', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER)))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("<b>Beyond Keywords. Beyond Filters. Pure Relevance.</b>", ParagraphStyle('tagline', parent=styles['Normal'], fontSize=13, alignment=TA_CENTER, textColor=HexColor('#f5576c'))))
story.append(PageBreak())

# Slide 2: Problem
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("The Problem", heading_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("<b>Recruiters lose hidden talent in the noise.</b>", body_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("❌ Keyword matching misses contextual fit", bullet_style))
story.append(Paragraph("❌ Behavioral signals are invisible to traditional filters", bullet_style))
story.append(Paragraph("❌ Manual screening of 100K+ profiles is impossible", bullet_style))
story.append(Paragraph("❌ Career trajectory and intent remain hidden", bullet_style))
story.append(Spacer(1, 0.4*inch))
story.append(Paragraph("<b>We built an AI brain that sees what humans see — but at scale.</b>", body_style))
story.append(PageBreak())

# Slide 3: Solution
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Our Solution: 4-Stage Pipeline", heading_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("<b>Stage 1:</b> Honeypot Detection — Filter fake profiles & timeline paradoxes", bullet_style))
story.append(Paragraph("<b>Stage 2:</b> Tier Gating — Suppress juniors if role demands mid/senior", bullet_style))
story.append(Paragraph("<b>Stage 3:</b> Weighted Scoring — Apply 8 signals; compute 0-1 scores", bullet_style))
story.append(Paragraph("<b>Stage 4:</b> Penalties & Multipliers — Boost strong matches, penalize weak fit", bullet_style))
story.append(Spacer(1, 0.4*inch))
story.append(Paragraph("<b>Result:</b> Deterministic, explainable top 100 shortlist in 60-90 seconds on CPU", body_style))
story.append(PageBreak())

# Slide 4: 8 Signals
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("8 Signals Driving Relevance", heading_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("📈 <b>Career Progression (20%)</b> — Role growth, seniority climb, lateral moves", bullet_style))
story.append(Paragraph("🎯 <b>Skills Match (22%)</b> — Semantic + exact skill alignment to JD", bullet_style))
story.append(Paragraph("📄 <b>JD Fit (15%)</b> — Deep semantic understanding of job requirements", bullet_style))
story.append(Paragraph("🏆 <b>Title Tier (15%)</b> — Seniority alignment & tier gating", bullet_style))
story.append(Paragraph("⏳ <b>Experience (10%)</b> — Years in role, depth, breadth", bullet_style))
story.append(Paragraph("🤝 <b>Behavioral (10%)</b> — Response rates, activity patterns", bullet_style))
story.append(Paragraph("📍 <b>Location (4%)</b> — Geography relevance, mobility", bullet_style))
story.append(Paragraph("🐙 <b>GitHub Signal (4%)</b> — Developer activity, contribution frequency", bullet_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("<b>Total: 1.0 (100% weighted sum)</b>", body_style))
story.append(PageBreak())

# Slide 5: Pipeline Stages
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Pipeline: Stage by Stage", heading_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("<b>Stage 1 | Honeypot & Timeline Detection</b>", bullet_style))
story.append(Paragraph("Filter out fake profiles & resume paradoxes (graduation dates, conflicting timelines)", ParagraphStyle('sub_bullet', parent=styles['Normal'], fontSize=10, leftIndent=40, spaceAfter=8)))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>Stage 2 | Tier Gating</b>", bullet_style))
story.append(Paragraph("Suppress Tier C (junior) candidates if role demands Tier A/B (mid/senior)", ParagraphStyle('sub_bullet', parent=styles['Normal'], fontSize=10, leftIndent=40, spaceAfter=8)))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>Stage 3 | Weighted Scoring</b>", bullet_style))
story.append(Paragraph("Apply 8 signals with configurable weights; compute 0-1 normalized scores", ParagraphStyle('sub_bullet', parent=styles['Normal'], fontSize=10, leftIndent=40, spaceAfter=8)))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>Stage 4 | Multipliers & Penalties</b>", bullet_style))
story.append(Paragraph("Boost strong matches, penalize weak fit; finalize top 100 shortlist", ParagraphStyle('sub_bullet', parent=styles['Normal'], fontSize=10, leftIndent=40, spaceAfter=8)))
story.append(PageBreak())

# Slide 6: Results
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Results & Performance", heading_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("<b>100,000 candidates processed in 60-90 seconds</b>", body_style))
story.append(Paragraph("<b>Zero external dependencies (pure Python 3.10+)</b>", body_style))
story.append(Paragraph("<b>Fully deterministic & reproducible</b>", body_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("<b>Top 5 Candidates (Sample Output)</b>", ParagraphStyle('label', parent=styles['Normal'], fontSize=12, fontName='Helvetica-Bold')))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("🥇 <b>#1:</b> Senior ML Engineer (7.2y) | Score: 0.9857", bullet_style))
story.append(Paragraph("🥈 <b>#2:</b> Search Engineer (7.6y) | Score: 0.9681", bullet_style))
story.append(Paragraph("🥉 <b>#3:</b> Senior NLP Engineer (7.8y) | Score: 0.9666", bullet_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("<b>Output Format:</b> CSV with candidate_id, rank, score, reasoning", body_style))
story.append(PageBreak())

# Slide 7: Technical Stack
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Technical Stack", heading_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("<b>Backend Ranking Engine</b>", ParagraphStyle('label', parent=styles['Normal'], fontSize=12, fontName='Helvetica-Bold')))
story.append(Paragraph("Pure Python 3.10+ | ~500 LOC | Zero external dependencies | Multi-threaded processing", bullet_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("<b>Frontend Sandbox</b>", ParagraphStyle('label', parent=styles['Normal'], fontSize=12, fontName='Helvetica-Bold')))
story.append(Paragraph("React 19 + TypeScript | Vite 6 | TailwindCSS 4 | Live weight calibration & export", bullet_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("<b>Reproducibility</b>", ParagraphStyle('label', parent=styles['Normal'], fontSize=12, fontName='Helvetica-Bold')))
story.append(Paragraph("<code>python rank.py --candidates &lt;dataset&gt; --out submission.csv</code>", bullet_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Runs on CPU. No GPUs, no cloud APIs, no rate limits. Fully offline.", body_style))
story.append(PageBreak())

# Slide 8: Why This Approach
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Why This Approach Wins", heading_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("✅ <b>Semantic Understanding:</b> Beyond keywords to true relevance", bullet_style))
story.append(Paragraph("✅ <b>Explainable Ranking:</b> Every candidate has clear reasoning", bullet_style))
story.append(Paragraph("✅ <b>Configurable Weights:</b> Adjust 8 signals for different roles", bullet_style))
story.append(Paragraph("✅ <b>Fast & Deterministic:</b> Runs in under 2 minutes on 100K profiles", bullet_style))
story.append(Paragraph("✅ <b>Production-Ready:</b> No ML framework bloat, pure algorithmic power", bullet_style))
story.append(Paragraph("✅ <b>Scalable:</b> Proven on 100K+ candidates; runs locally on CPU", bullet_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("<b>The result: Recruiters get a curated, ranked shortlist they can trust.</b>", ParagraphStyle('highlight', parent=styles['Normal'], fontSize=12, textColor=HexColor('#f5576c'), alignment=TA_CENTER)))

# Build PDF
doc.build(story)
print(f"✓ PDF presentation generated: {pdf_file}")
