from cs50 import SQL

db = SQL("sqlite:///ortho.db")

words =  db.execute("SELECT mot FROM words WHERE nb_syllabes = ? AND difficulte = ? ORDER BY RANDOM() LIMIT 10",2,3)

print(words)
