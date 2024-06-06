import csv  # Module pour la manipulation de fichiers CSV

# Importations PyQt6 pour l'interface graphique
from PySide6.QtWidgets import QMessageBox

def importer_csv(self, nom_fichier):
    if nom_fichier:
        try:
            with open(nom_fichier, newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=';')
                self.delegue_master.recup_onglet_eleves().effacer_table()

                # Ignorer la première ligne (en-tête)
                next(csvreader)

                for row, data in enumerate(csvreader):
                    self.delegue_master.recup_onglet_eleves().ajouter_eleve(data[0], data[1])

            QMessageBox.information(self.delegue_master, tr('succes'),tr('donnes_importees') + nom_fichier)
        except Exception as e: QMessageBox.critical(self.delegue_master, tr('erreur'),tr('message_erreur') + str(e))


def exporter_csv(delegue_master, nom_fichier):
    tr = delegue_master.langues.tr
    if nom_fichier:
            try:
                QMessageBox.information(delegue_master, tr('succes'),
                                        tr('donnes_exportees') + nom_fichier)
            except Exception as e:
                QMessageBox.critical(delegue_master, tr('erreur'), tr('message_erreur') + str(e))
                
                QMessageBox.information(delegue_master, tr('succes'),
                                        tr('donnes_exportees') + nom_fichier)
            except Exception as e:
                QMessageBox.critical(delegue_master, tr('erreur'), tr('message_erreur') + str(e))
