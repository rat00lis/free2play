import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('free2play.db')

# Crear tabla tcg
conn.execute('''
    CREATE TABLE Tcg(
        tcg_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tcg_name TEXT NOT NULL,
        tcg_description TEXT 
    )
''')

# Crear tabla de productos
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

# Crear tabla usuario
conn.execute('''
    CREATE TABLE User(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        user_mail TEXT UNIQUE NOT NULL,
        user_pass TEXT NOT NULL
    )
''')

# Crear tabla de pedido
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

# Insertar datos de ejemplo en Tcg
conn.execute('''
    INSERT INTO Tcg (tcg_name, tcg_description) VALUES 
    ('Magic The Gathering', 'A popular trading card game'),
    ('Yu-Gi-Oh!', 'A trading card game based on the Yu-Gi-Oh! anime series')
''')

# Insertar productos de ejemplo en Card
conn.execute('''
    INSERT INTO Card (card_tcg, card_name, card_edition, card_treatment, card_language, card_condition, card_availability, card_price, card_image) VALUES 
    (1, 'Black Lotus', 'Alpha', 'Foil', 'English', 'NM', 1, 100000.00, 'https://www.paytowin.cl/cdn/shop/products/4efac807-954e-5e4e-ba9e-445bce58a82a_800x.jpg?v=1663896993'),
    (1, 'Mox Sapphire', 'Beta', 'Non-Foil', 'English', 'EX', 2, 50000.00, 'https://www.paytowin.cl/cdn/shop/products/cff5d45e-4e7b-5b80-bb4c-0d3da090e209_800x.jpg?v=1663900324'),
    (1, 'Ancestral Recall', 'Unlimited', 'Foil', 'English', 'NM', 3, 30000.00, 'https://www.paytowin.cl/cdn/shop/products/36c35d71-a57e-5878-a90a-2f8347a42972_800x.jpg?v=1663890721'),
    (1, 'Time Walk', 'Alpha', 'Non-Foil', 'English', 'G', 1, 20000.00, 'https://www.paytowin.cl/cdn/shop/products/79d5ffee-fd19-5351-b41d-4d076545c92d_800x.jpg?v=1663896738'),
    (1, 'Timetwister', 'Beta', 'Foil', 'English', 'PLD', 2, 15000.00, 'https://www.paytowin.cl/cdn/shop/products/c3ab1501-b5a3-55de-9e4f-b82ec3371f71_f56f5c47-9aeb-4e97-916f-6a56b18d5f80_800x.jpg?v=1663890207'),
    (2, 'Blue-Eyes White Dragon', 'First Edition', 'Foil', 'Japanese', 'NM', 5, 1000.00, 'https://cdnx.jumpseller.com/deckscards/image/9338504/1193980.jpg?1653505707'),
    (2, 'Dark Magician', 'First Edition', 'Non-Foil', 'Japanese', 'EX', 4, 800.00, 'https://cdnx.jumpseller.com/deckscards/image/38570460/46986414.jpg?1692309347'),
    (2, 'Red-Eyes Black Dragon', 'First Edition', 'Foil', 'Japanese', 'NM', 3, 600.00, 'https://cdnx.jumpseller.com/deckscards/image/38570592/74677422.jpg?1692309467'),
    (2, 'Exodia the Forbidden One', 'First Edition', 'Non-Foil', 'Japanese', 'G', 1, 500.00, 'https://mesa1.cl/cdn/shop/products/a10a6965-c151-58b9-8ec1-1d4796e316ef_800x.png?v=1622425779'),
    (2, 'Blue-Eyes Ultimate Dragon', 'First Edition', 'Foil', 'Japanese', 'NM', 2, 1200.00, 'https://mesa1.cl/cdn/shop/products/0f6ab3de-3709-5631-8e98-f64f15b3ac48_800x.png?v=1622424425')
''')

conn.commit()
conn.close()
