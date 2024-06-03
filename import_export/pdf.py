<<<<<<< HEAD
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
=======
# Importations PyQt6 pour l'interface graphique
from PySide6.QtWidgets import QMessageBox, QFileDialog
# Importation de la fonction pour appliquer un thème à l'interface
from qt_material import apply_stylesheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from utils.files_utils import get_assets_path

def exporter_pdf(delegue_master, tr, checkboxs, dialog):
    try:
        # Continuer avec l'exportation selon les choix de l'utilisateur
        dossier_pdf, _ = QFileDialog.getSaveFileName(delegue_master, tr('exporter_pdf'), tr('conseils'),
                                                             'PDF Files (*.pdf)')
        if dossier_pdf:
                    
            # Renseignement de la police de caractères pour l'export PDF
            police = get_assets_path("Roboto-Regular.ttf")
            pdfmetrics.registerFont(TTFont('Roboto-Regular', police))
                    
            # Création d'un document PDF avec encodage UTF-8 et la police Plex Mono
            doc = SimpleDocTemplate(dossier_pdf, pagesize=letter, encoding='utf-8')

            # Style pour le texte en gras
            styles = getSampleStyleSheet()
            bold_style = styles['Normal']
            bold_style.fontName = 'Roboto-Regular'

            # Contenu du document PDF
            elements = []
                    
            # Style du tableau
            table_style = TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])
>>>>>>> dc682bbcb658d6e2427319f7e6d1c93c16bddda1

            eleves = delegue_master.getClasse().get_eleves()

            for eleve in eleves:
<<<<<<< HEAD
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
=======
                # Création du tableau pour chaque élève
                data = [
                [Paragraph('<b>' + eleve.get_nom_complet() + '</b>', bold_style),
                Paragraph(tr('remarque'), styles['Normal']),
                Paragraph(tr('moyenne'), styles['Normal']),
                Paragraph(tr('mention'), styles['Normal'])]
                ]
                
                for i in range(len(eleve.get_periodes())):
                    if checkboxs[i].isChecked():
                        periode = eleve.get_periode(i)
                        data.append([
                        Paragraph("Période " + str(i+1), styles['Normal']),
                        Paragraph(periode.get_remarque() if periode.get_remarque() else "", styles['Normal']),
                        Paragraph(str(periode.get_moyenne() if periode.get_moyenne() is not None else "0.0"), styles['Normal']),
                        Paragraph(tr('appreciations')[periode.get_appreciation()] if periode.get_appreciation() else tr('appreciations')[0], styles['Normal'])
                        ])

                # Création du tableau
                table = Table(data)
                table.setStyle(table_style)

                # Ajout du tableau au contenu du PDF
                elements.append(table)

                # Ajout d'un espace entre chaque élève
                elements.append(Spacer(1, 12))

            # Génération du PDF
            doc.build(elements)

            QMessageBox.information(delegue_master, tr('succes'), tr('message_pdf') + dossier_pdf)

            dialog.close()
    except Exception as e:
        QMessageBox.critical(delegue_master, tr('erreur'), tr('message_erreur') + str(e))
                
>>>>>>> dc682bbcb658d6e2427319f7e6d1c93c16bddda1
