import csv
from cs50 import SQL

# Connect to the database
db = SQL("sqlite:///ortho.db")

def main():

    increment_db("words.csv")


# ajouter ail eil euil ouil / cr br fr vr pr / suffixe ssion eur euse tion / ajouter log mot?
 # calcul du nombre de voyelles
def calculer_difficulte_mot(mot, nb_syllabes):

    # Présence de consonnes complexes
    consonnes_complexes = ["tr", "gr", "fr","pr","pl","gl","pt"]  # Exemple de consonnes complexes
    nb_consonnes_complexes = sum(mot.count(cc) for cc in consonnes_complexes)

    # Présence de voyelles nasales
    voyelles_nasales = ["en", "on", "an","ain","ouin",]  # Exemple de voyelles nasales
    nb_voyelles_nasales = sum(mot.count(vn) for vn in voyelles_nasales)

    # Calcul de la difficulté totale
    difficulte = nb_syllabes + nb_consonnes_complexes + nb_voyelles_nasales

    return difficulte

def compter_syllabes(mot):
    # Simple méthode de comptage des syllabes (peut ne pas être précise dans tous les cas)
    syllabes = 0
    voyelles = "aeiouyAEIOUY"
    pre_voyelle = False

    if(len(mot)==1):  # pour mes mots a 1 caractere
        syllabes += 1
        return syllabes

    for lettre in mot:
        if lettre in voyelles:
            if not pre_voyelle:
                syllabes += 1
            pre_voyelle = True
        else:
            pre_voyelle = False
    return syllabes

def freq_aprox(frequence): # from 0 to 1 000 000
    if frequence < 1000:
        return 'élevée'
    if frequence > 1000 and frequence < 10000:
        return 'moyenne'
    if frequence >10000 and frequence < 100000:
        return 'faible'
    if frequence >100000:
        return 'très faible'

def increment_db(csv_file):
    # Open the CSV file containing the words
    with open(csv_file, "r") as file:
        # Create a CSV reader object
        reader = csv.reader(file)

         # Skip the header row
        next(reader)

        # Iterate over each row in the CSV file
        for row in reader:



            # Ensure that the row has at least 3 elements
            if len(row) >= 3:
                # Extract data from the row
                nature = row[0]
                frequence = freq_aprox(int(row[1]))
                mot = " ".join(row[2:])  # Join remaining elements as the word
                nb_syllabes = compter_syllabes(mot)
                difficulte = calculer_difficulte_mot(mot, nb_syllabes)

            # Insert the data into the database
            db.execute("INSERT INTO words (nature, frequence, mot, nb_syllabes, difficulte) VALUES (?, ?, ?, ?, ?)", nature, frequence, mot, nb_syllabes, difficulte)

main()
