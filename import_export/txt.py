import os

from PySide6.QtWidgets import QMessageBox

def importer_txt(delegue_master, nom_fichier):
    tr = delegue_master.langues.tr
    if nom_fichier:
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as txtfile:
                delegue_master.recup_onglet_eleves().effacer_table()

                for line in txtfile:
                    data = line.strip().split(' ')
                    delegue_master.recup_onglet_eleves().ajouter_eleve(data[0], data[1])

            QMessageBox.information(delegue_master, tr('succes'), tr('donnes_importees') + nom_fichier)
        except Exception as e:
            QMessageBox.critical(delegue_master, tr('erreur'), tr('message_erreur') + str(e))
                

def exporter_txt(delegue_master, nom_fichier, periodes_checkboxs, par_classe):
    tr = delegue_master.langues.tr
    if nom_fichier:
        try:
            classe = delegue_master.getClasse()
            eleves = classe.get_eleves()

            for eleve in eleves:
                nom_fichier_eleve = os.path.join(nom_fichier, f"{eleve.get_nom_complet()}.txt")

                with open(nom_fichier_eleve, 'w', encoding='utf-8') as txtfile:
                    appreciations = tr('appreciations')
                    for appreciation in delegue_master.profile.appreciations:
                        appreciations.append(appreciation)
                    for i in range(len(periodes_checkboxs)):
                        if periodes_checkboxs[i].isChecked():
                            periode = eleve.get_periode(i)
                            if len(periodes_checkboxs) > 0:
                                if len(periodes_checkboxs) != 1:
                                    txtfile.write(f"Période: {i+1}/{len(periodes_checkboxs)}\n")
                                txtfile.write(f"Remarque: {periode.get_remarque()}\n")  # Remarque à compléter
                                txtfile.write(f"Moyenne: {periode.get_moyenne()}\n")  # Moyenne à compléter
                                txtfile.write(f"Appréciations: {appreciations[periode.get_appreciation()]} \n")  # Appréciations à compléter
                                if len(periodes_checkboxs) != 1 or len(periodes_checkboxs) - 1 != i:
                                    txtfile.write("\n")

            QMessageBox.information(delegue_master, tr('succes'), tr('donnes_exportees') + nom_fichier)
        except Exception as e:
            QMessageBox.critical(delegue_master, tr('erreur'), tr('message_erreur') + str(e))
