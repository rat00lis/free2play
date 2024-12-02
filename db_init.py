import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('free2play.db')

# Crear tabla Tcg
conn.execute('''
    CREATE TABLE Tcg(
        tcg_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tcg_name TEXT NOT NULL,
        tcg_description TEXT
    )
''')

# Crear tabla Card
conn.execute('''
    CREATE TABLE Card (
        card_id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_tcg INTEGER NOT NULL, 
        card_name TEXT NOT NULL,
        card_edition TEXT NOT NULL,
        card_treatment TEXT NOT NULL,
        card_language TEXT NOT NULL,
        card_condition TEXT CHECK(card_condition IN('NM', 'EX', 'G', 'PLD', 'HP')) NOT NULL,
        card_availability INTEGER NOT NULL,
        card_price REAL NOT NULL,
        card_image TEXT,
        FOREIGN KEY (card_tcg) REFERENCES Tcg(tcg_id)
    )
''')

# Crear tabla User
conn.execute('''
    CREATE TABLE User(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        user_mail TEXT UNIQUE NOT NULL,
        user_pass TEXT NOT NULL
    )
''')

# Crear tabla Purchase
conn.execute('''
    CREATE TABLE Purchase (
        purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        purchase_date DATE DEFAULT CURRENT_DATE,
        purchase_total REAL NOT NULL,
        card_id INTEGER NOT NULL,
        card_amount INTEGER NOT NULL,
        FOREIGN KEY (card_id) REFERENCES Card(card_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
''')

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()
