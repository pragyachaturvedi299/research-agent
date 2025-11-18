from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime


def save_pdf(query, sub_questions, search_results, final_answer, eval_metrics, file_name,config):
    """
    Create a clean and professional PDF report for the research output.
    """

    
    doc = SimpleDocTemplate(
        file_name,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    # ---------------------------- Custom Styles ----------------------------
    title_style = ParagraphStyle(
        "title_style",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    header_style = ParagraphStyle(
        "header_style",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "body_style",
        parent=styles["BodyText"],
        fontSize=11,
        leading=15,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        "bullet_style",
        parent=styles["BodyText"],
        fontSize=11,
        leading=14,
        leftIndent=20,
        spaceAfter=4
    )

    # ---------------------------- Build Content ----------------------------
    elements = []

    # Title page
    elements.append(Paragraph("Deep Research Report", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"<b>Query:</b> {query}", body_style))
    elements.append(Spacer(1, 15))

    # Sub-Questions
    elements.append(Paragraph("Sub-Questions", header_style))
    for sq in sub_questions:
        elements.append(Paragraph(f"• {sq}", bullet_style))

    elements.append(PageBreak())

    # Search Summary
    elements.append(Paragraph("Search Results Summary", header_style))
    for result in search_results:
        clean_result = str(result).replace("{", "").replace("}", "")
        elements.append(Paragraph(clean_result, body_style))

    elements.append(PageBreak())

    # Final Synthesized Research
    elements.append(Paragraph("Final Synthesized Answer", header_style))
    for paragraph in final_answer.split("\n"):
        if paragraph.strip():
            elements.append(Paragraph(paragraph, body_style))

    elements.append(PageBreak())

    # Evaluation Metrics in Table Format
    elements.append(Paragraph("Evaluation Metrics", header_style))

    table_data = [
        ["Metric", "Score"],
        ["Completeness", eval_metrics.get("Completeness", "")],
        ["Relevance", eval_metrics.get("Relevance", "")],
        ["Accuracy", eval_metrics.get("Accuracy", "")],
        ["Structure & Clarity", eval_metrics.get("Clarity", "")],
        ["Hallucination Risk", eval_metrics.get("Hallucination Risk", "")]
    ]

    table = Table(table_data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f2f2f2")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Footer note
    elements.append(Paragraph(
        "<i>This report was auto-generated using a Deep Research Agent powered by LangChain & OpenAI.</i>",
        ParagraphStyle("footer", fontSize=9, alignment=TA_CENTER)
    ))

    # ---------------------------- Build PDF ----------------------------
    doc.build(elements)

    print(f"[INFO] PDF generated successfully: {file_name}")
    return file_name
