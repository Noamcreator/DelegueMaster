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

            eleves = delegue_master.getClasse().get_eleves()

            for eleve in eleves:
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
                