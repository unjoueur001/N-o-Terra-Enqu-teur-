import random
import json
import os

class Suspect:
    def __init__(self, nom, statut, crime, preuves):
        self.nom = nom
        self.statut = statut  # "innocent" ou "coupable"
        self.crime = crime
        self.preuves = preuves
        self.reponses = {
            "innocent": [
                "Je suis innocent, je vous le jure!",
                "Je n'ai rien fait de mal.",
                "Vous devez me croire, je suis innocent."
            ],
            "coupable": [
                "Je ne sais pas de quoi vous parlez.",
                "C'est un malentendu.",
                "Je n'ai rien à dire."
            ]
        }

    def repondre(self):
        return random.choice(self.reponses[self.statut])

class DossierEnquete:
    def __init__(self):
        self.dossiers = {
            "Alice": {
                "crime": "Vol à la tire",
                "preuves": ["Témoignage", "Vidéo surveillance"],
                "statut": "innocent"
            },
            "Bob": {
                "crime": "Braquage de banque",
                "preuves": ["Arme retrouvée", "Témoignage"],
                "statut": "coupable"
            },
            "Charlie": {
                "crime": "Meurtre",
                "preuves": ["Arme du crime", "Témoignage", "Empreintes digitales"],
                "statut": "coupable"
            },
            "David": {
                "crime": "Escroquerie",
                "preuves": ["Documents falsifiés", "Témoignage"],
                "statut": "innocent"
            },
            "Eve": {
                "crime": "Trafic de drogues",
                "preuves": ["Drogues trouvées", "Témoignage", "Messages téléphoniques"],
                "statut": "coupable"
            },
            "Frank": {
                "crime": "Fraude",
                "preuves": ["Documents falsifiés", "Témoignage", "Transactions suspectes"],
                "statut": "innocent"
            }
        }

    def consulter_dossier(self, nom):
        if nom in self.dossiers:
            dossier = self.dossiers[nom]
            print(f"Dossier de {nom}:")
            print(f"Crime: {dossier['crime']}")
            print(f"Preuves: {', '.join(dossier['preuves'])}")
            print(f"Statut: {dossier['statut']}")
        else:
            print("Dossier non trouvé.")

class PNJ:
    def __init__(self, nom, role, dialogue, consequence_accept, consequence_refuse):
        self.nom = nom
        self.role = role
        self.dialogue = dialogue
        self.consequence_accept = consequence_accept
        self.consequence_refuse = consequence_refuse

    def parler(self):
        print(f"{self.nom}: {self.dialogue}")

    def interagir(self, joueur):
        self.parler()
        choix = input("Accepter la demande? (oui/non): ")
        if choix.lower() == "oui":
            print(self.consequence_accept)
            if "virus" in self.consequence_accept:
                joueur.inventaire.append("bocal avec virus")
                print("Vous avez ajouté le bocal à votre inventaire.")
        else:
            print(self.consequence_refuse)

class Quest:
    def __init__(self, description, recompense):
        self.description = description
        self.recompense = recompense
        self.complete = False

    def completer(self, joueur):
        self.complete = True
        joueur.score += self.recompense
        print(f"Quête complétée! Vous avez gagné {self.recompense} points.")

class Enqueteur:
    def __init__(self):
        self.score = 0
        self.reputation = 0
        self.dossier_enquete = DossierEnquete()
        self.corrompu = False
        self.titres = []
        self.niveau = 1
        self.competences = {
            "interrogation": 1,
            "analyse_preuves": 1,
            "persuasion": 1
        }
        self.inventaire = []
        self.quests = [
            Quest("Trouver le bocal avec le virus", 10),
            Quest("Résoudre 5 affaires avec succès", 20),
            Quest("Atteindre une réputation de 50", 30)
        ]

    def consulter_dossier(self, nom):
        self.dossier_enquete.consulter_dossier(nom)

    def poser_question(self, suspect):
        print(f"{suspect.nom}: {suspect.repondre()}")

    def juger(self, suspect, jugement):
        if jugement == suspect.statut:
            self.score += 1
            self.reputation += 1
            print("Bonne décision!")
            if jugement == "coupable":
                self.choisir_peine(suspect)
        else:
            self.score -= 1
            self.reputation -= 1
            print("Mauvaise décision!")

    def choisir_peine(self, suspect):
        print(f"Choisissez une peine pour {suspect.nom} :")
        print("1. Amende")
        print("2. Prison")
        print("3. Travail d'intérêt général")
        choix = input("Entrez le numéro de la peine: ")
        peines = {
            "1": "Amende",
            "2": "Prison",
            "3": "Travail d'intérêt général"
        }
        peine = peines.get(choix, "Amende")
        print(f"You have chosen {peine} for {suspect.nom}.")

    def interagir_avec_pnj(self, pnj):
        pnj.interagir(self)

    def ameliorer_competence(self, competence):
        if competence in self.competences:
            self.competences[competence] += 1
            print(f"Compétence {competence} améliorée!")
        else:
            print("Compétence non valide.")

    def monter_niveau(self):
        if self.score >= self.niveau * 10:
            self.niveau += 1
            print(f"Félicitations! Vous êtes maintenant au niveau {self.niveau}.")
            return True
        else:
            print("Vous n'avez pas assez de points pour monter de niveau.")
            return False

    def obtenir_titre(self):
        if self.corrompu:
            return "Corrompu"
        elif self.score >= 20:
            return "Maître Enquêteur"
        elif self.score >= 10:
            return "Enquêteur Expérimenté"
        else:
            return "Débutant"

    def ajouter_titre(self, titre):
        self.titres.append(titre)

    def verifier_fin_jeu(self):
        if self.reputation >= 100:
            print("Félicitations! Vous avez atteint une réputation excellente et avez terminé le jeu.")
            return True
        elif self.reputation <= -50:
            print("Vous avez une réputation trop basse et avez terminé le jeu.")
            return True
        else:
            return False

    def sauvegarder_partie(self, nom_fichier):
        data = {
            "score": self.score,
            "reputation": self.reputation,
            "corrompu": self.corrompu,
            "titres": self.titres,
            "niveau": self.niveau,
            "competences": self.competences,
            "inventaire": self.inventaire,
            "quests": [{"description": q.description, "complete": q.complete} for q in self.quests]
        }
        with open(nom_fichier, 'w') as f:
            json.dump(data, f)
        print(f"Partie sauvegardée dans {nom_fichier}.")

    def charger_partie(self, nom_fichier):
        if os.path.exists(nom_fichier):
            with open(nom_fichier, 'r') as f:
                data = json.load(f)
            self.score = data["score"]
            self.reputation = data["reputation"]
            self.corrompu = data["corrompu"]
            self.titres = data["titres"]
            self.niveau = data["niveau"]
            self.competences = data["competences"]
            self.inventaire = data["inventaire"]
            for q in data["quests"]:
                for quest in self.quests:
                    if quest.description == q["description"]:
                        quest.complete = q["complete"]
            print(f"Partie chargée depuis {nom_fichier}.")
        else:
            print("Fichier de sauvegarde non trouvé.")

# Exemple d'utilisation
suspect1 = Suspect("Alice", "innocent", "Vol à la tire", ["Témoignage", "Vidéo surveillance"])
suspect2 = Suspect("Bob", "coupable", "Braquage de banque", ["Arme retrouvée", "Témoignage"])
suspect3 = Suspect("Charlie", "coupable", "Meurtre", ["Arme du crime", "Témoignage", "Empreintes digitales"])
suspect4 = Suspect("David", "innocent", "Escroquerie", ["Documents falsifiés", "Témoignage"])
suspect5 = Suspect("Eve", "coupable", "Trafic de drogues", ["Drogues trouvées", "Témoignage", "Messages téléphoniques"])
suspect6 = Suspect("Frank", "innocent", "Fraude", ["Documents falsifiés", "Témoignage", "Transactions suspectes"])

pnj1 = PNJ("Conseiller", "conseiller", "Je pense que tu devrais vérifier les preuves plus attentivement.", "Bonne chance!", "Tu as refusé l'offre.")
pnj2 = PNJ("Corrupteur", "corrupteur", "Je peux t'offrir des points supplémentaires si tu me fais une faveur.", "Tu as accepté l'offre. Ton score a augmenté, mais tu es maintenant corrompu.", "Tu as refusé l'offre.")
pnj3 = PNJ("Témoin", "témoin", "J'ai vu quelque chose de suspect.", "Merci pour ton aide!", "Tu as refusé l'offre.")
pnj4 = PNJ("Avocat", "avocat", "Mon client est innocent, je vous le jure.", "Merci pour ton aide!", "Tu as refusé l'offre.")
pnj5 = PNJ("Juge", "juge", "Assurez-vous de suivre les procédures légales.", "Bonne chance!", "Tu as refusé l'offre.")
pnj6 = PNJ("Inconnu", "demandeur", "Peux-tu garder ce bocal pour moi? C'est très important.", "Tu as accepté de garder le bocal. Mais il contient le virus!", "Tu as refusé. L'inconnu part en disant que tu vas le regretter.")

enqueteur = Enqueteur()

enqueteur.consulter_dossier("Alice")
enqueteur.poser_question(suspect1)
enqueteur.juger(suspect1, "innocent")  # Le joueur juge le suspect

enqueteur.interagir_avec_pnj(pnj6)

enqueteur.interagir_avec_pnj(pnj1)
enqueteur.interagir_avec_pnj(pnj2)

enqueteur.consulter_dossier("Bob")
enqueteur.poser_question(suspect2)
enqueteur.juger(suspect2, "coupable")  # Le joueur juge le suspect

enqueteur.ameliorer_competence("interrogation")
enqueteur.monter_niveau()

print(f"Score final: {enqueteur.score}")
print(f"Réputation: {enqueteur.reputation}")
print(f"Titres: {', '.join(enqueteur.titres)}")
print(f"Titre principal: {enqueteur.obtenir_titre()}")

if enqueteur.verifier_fin_jeu():
    print("Fin du jeu.")
