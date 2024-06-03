from PySide6.QtWidgets import QMessageBox, QFileDialog
from qt_material import apply_stylesheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
from reportlab.pdfgen import canvas

from utils.files_utils import get_assets_path

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        super().showPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 10)
        page_num = self._pageNumber
        text = f"{page_num}/{page_count}"
        self.drawCentredString(self._pagesize[0] / 2.0, 10 * mm, text)

def exporter_pdf(delegue_master, dossier_pdf, periodes_checkboxs, dialog):
    tr = delegue_master.langues.tr
    try:
        if dossier_pdf:
            roboto = get_assets_path('fonts/Roboto/Roboto-')
            roboto_bold = roboto + 'Bold.ttf'
            roboto_regular = roboto + 'Regular.ttf'
            pdfmetrics.registerFont(TTFont('Roboto-Bold', roboto_bold))
            pdfmetrics.registerFont(TTFont('Roboto-Regular', roboto_regular))

            doc = SimpleDocTemplate(dossier_pdf, pagesize=letter, encoding='utf-8',
                                    leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                                    topMargin=0.5 * inch, bottomMargin=0.5 * inch)

            styles = getSampleStyleSheet()
            bold_style = ParagraphStyle(
                'BoldStyle',
                parent=styles['Normal'],
                fontName='Roboto-Bold',
                valign='top'
            )
            
            normal_style = ParagraphStyle(
                'NormalStyle',
                parent=styles['Normal'],
                fontName='Roboto-Regular',
                valign='top'
            )

            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Title'],
                fontName='Roboto-Bold',
                fontSize=22,
                leading=26
            )

            elements = []

            title = Paragraph('Conseils de Classe de la ' + delegue_master.getClasse().get_nom(), title_style)
            elements.append(title)
            elements.append(Spacer(1, 12))

            table_style = TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ])

            eleves = delegue_master.getClasse().get_eleves()

            for eleve in eleves:
                data = [
                    [Paragraph('<b>' + eleve.get_nom_complet() + '</b>', bold_style),
                     Paragraph(tr('remarque'), normal_style),
                     Paragraph(tr('moyenne'), normal_style),
                     Paragraph(tr('mention'), normal_style)]
                ]

                for i in range(len(eleve.get_periodes())):
                    if periodes_checkboxs[i].isChecked():
                        periode = eleve.get_periode(i)
                        data.append([
                            Paragraph("Période " + str(i+1), normal_style),
                            Paragraph(periode.get_remarque() if periode.get_remarque() else "", normal_style),
                            Paragraph(str(periode.get_moyenne() if periode.get_moyenne() is not None else "0.0"), normal_style),
                            Paragraph(tr('appreciations')[periode.get_appreciation()] if periode.get_appreciation() else tr('appreciations')[0], normal_style)
                        ])

                table = Table(data)
                table.setStyle(table_style)

                elements.append(KeepTogether(table))
                elements.append(Spacer(1, 12))

            doc.build(elements, canvasmaker=NumberedCanvas)

            QMessageBox.information(delegue_master, tr('succes'), tr('message_pdf') + dossier_pdf)
            dialog.close()
        else:
            dossier_pdf, _ = QFileDialog.getSaveFileName(delegue_master, tr('exporter_pdf'), tr('conseils'),
                                                     'PDF Files (*.pdf)')
            exporter_pdf(delegue_master, dossier_pdf, periodes_checkboxs, dialog)
    except Exception as e:
        QMessageBox.critical(delegue_master, tr('erreur'), tr('message_erreur') + str(e))
