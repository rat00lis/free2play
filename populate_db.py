import sqlite3
import random

# Configuración inicial
NUM_CARDS = 1000  # Número de cartas a insertar
NUM_USERS = 500   # Número de usuarios a insertar
NUM_PURCHASES = 2000  # Número de compras a insertar

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('free2play.db')
    conn.row_factory = sqlite3.Row
    return conn

# Listas de nombres y atributos para generar cartas
tcg_names = ["Magic The Gathering", "Yu-Gi-Oh!", "Pokemon TCG", "Digimon Card Game", "Flesh and Blood"]
card_editions = ["Alpha", "Beta", "Unlimited", "First Edition", "Collector's Edition"]
card_treatments = ["Foil", "Non-Foil"]
card_languages = ["English", "Japanese", "Spanish", "German", "French"]
card_conditions = ["NM", "EX", "G", "PLD", "HP"]
card_names = [
    "Dragon", "Phoenix", "Knight", "Wizard", "Elemental", "Beast", "Elf", "Zombie", 
    "Goblin", "Angel", "Vampire", "Demon", "Shaman", "Giant", "Witch", "Warlock", 
    "Troll", "Dwarf", "Orc", "Sprite", "Serpent", "Hydra", "Lich", "Harpy", 
    "Griffin", "Chimera", "Golem", "Djinn", "Fae", "Merfolk", "Kraken", "Centaur", 
    "Minotaur", "Slime", "Cyclops", "Basilisk", "Wraith", "Banshee", "Dryad", 
    "Treant", "Nymph", "Sphinx", "Wurm", "Shade", "Rogue", "Assassin", "Paladin", 
    "Sorcerer", "Necromancer", "Cleric", "Bard", "Hunter", "Monk", "Samurai", 
    "Ninja", "Pirate", "Templar", "Barbarian", "Guardian", "Sentinel", "Invoker", 
    "Seer", "Prophet", "Oracle", "Champion", "Conqueror", "Emperor", "Lancer"
]
adjectives = [
    "Mighty", "Ancient", "Infernal", "Celestial", "Furious", "Eternal", 
    "Cunning", "Fearless", "Shadowy", "Radiant", "Savage", "Noble", 
    "Wicked", "Chaotic", "Luminous", "Venomous", "Armored", "Blazing", 
    "Frozen", "Thunderous", "Silent", "Swift", "Graceful", "Ruthless", 
    "Holy", "Unholy", "Feral", "Mystic", "Void", "Abyssal", "Doomed", 
    "Enchanted", "Wild", "Cursed", "Blessed", "Corrupted", "Resilient", 
    "Vengeful", "Ethereal", "Bold", "Phantom", "Spectral", "Unyielding", 
    "Dominant", "Swiftfooted", "Shattered", "Primordial", "Runic", 
    "Howling", "Shimmering", "Gilded", "Piercing", "Hallowed", "Exalted"
]


# Generar datos ficticios
def generate_cards(num_cards):
    cards = []
    for _ in range(num_cards):
        card = (
            random.randint(1, len(tcg_names)),  # tcg_id
            f"{random.choice(adjectives)} {random.choice(card_names)}",  # card_name
            random.choice(card_editions),  # card_edition
            random.choice(card_treatments),  # card_treatment
            random.choice(card_languages),  # card_language
            random.choice(card_conditions),  # card_condition
            random.randint(1, 100),  # card_availability
            round(random.uniform(0.5, 500.0), 2),  # card_price
            "blank"  # card_image
        )
        cards.append(card)
    return cards


def generate_users(num_users):
    users = []
    for i in range(num_users):
        user = (
            f"user{i}@example.com",  # user_mail
            f"User {i}",  # user_name
            "password123"  # user_pass
        )
        users.append(user)
    return users

def generate_purchases(num_purchases, num_cards, num_users):
    purchases = []
    for _ in range(num_purchases):
        user_id = random.randint(1, num_users)
        card_id = random.randint(1, num_cards)
        card_amount = random.randint(1, 5)
        purchase_total = round(random.uniform(0.5, 500.0), 2) * card_amount
        purchase = (user_id, card_id, card_amount, purchase_total)
        purchases.append(purchase)
    return purchases

# Insertar datos en la base de datos
def insert_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insertar TCGs
    for i, tcg_name in enumerate(tcg_names, start=1):
        cursor.execute("INSERT OR IGNORE INTO Tcg (tcg_name, tcg_description) VALUES (?, ?)",
                       (tcg_name, f"{tcg_name} description"))

    # Insertar cartas
    cards = generate_cards(NUM_CARDS)
    cursor.executemany('''
        INSERT INTO Card (card_tcg, card_name, card_edition, card_treatment, card_language, 
        card_condition, card_availability, card_price, card_image) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', cards)

    # Insertar usuarios
    users = generate_users(NUM_USERS)
    cursor.executemany('''
        INSERT INTO User (user_mail, user_name, user_pass)
        VALUES (?, ?, ?)
    ''', users)

    # Insertar compras
    purchases = generate_purchases(NUM_PURCHASES, NUM_CARDS, NUM_USERS)
    cursor.executemany('''
        INSERT INTO Purchase (user_id, card_id, card_amount, purchase_total)
        VALUES (?, ?, ?, ?)
    ''', purchases)

    conn.commit()
    conn.close()

# Ejecutar inserción de datos
if __name__ == "__main__":
    insert_data()
    print(f"Datos insertados: {NUM_CARDS} cartas, {NUM_USERS} usuarios, {NUM_PURCHASES} compras.")
