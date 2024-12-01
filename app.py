from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('free2play.db')
    conn.row_factory = sqlite3.Row
    return conn

# Middleware para registrar la solicitud entrante
@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

# Middleware para registrar la respuesta saliente
@app.after_request
def log_response_info(response):
    app.logger.debug('Response status: %s', response.status)
    app.logger.debug('Response headers: %s', response.headers)
    return response

# Ruta para consultar productos
@app.route('/list_cards', methods=['GET'])
def list_cards():
    conn = get_db_connection()
    cards = conn.execute('SELECT * FROM Card').fetchall()
    conn.close()
    return render_template('list_cards.html', cards=cards)

# Ruta para registrar compra
@app.route('/buy', methods=['POST'])
def buy():
     #product_id = request.form.get('product_id')
    user_name = request.form.get('user_name')
    user_mail = request.form.get('user_mail')
    user_pass = request.form.get('user_pass')
    card_id = request.form.get('card_id')
    card_amount = request.form.get('card_amount')

    if not card_id or not user_name or not user_mail or not user_pass:
        return "Missing information", 400

    try:
        card_amount = int(card_amount)
        if card_amount <= 0:
            return "Invalid card amount", 400
    except ValueError:
        return "Invalid card amount", 400

    conn = get_db_connection()
    card = conn.execute('SELECT * FROM Card WHERE card_id = ?', (card_id,)).fetchone()
    if card is None:
        conn.close()
        return "Card not found", 404

    user = conn.execute('SELECT * FROM User WHERE user_mail = ?', (user_mail,)).fetchone()
    if user is None:
        conn.execute('INSERT INTO User (user_name, user_mail, user_pass) VALUES (?, ?, ?)', 
                     (user_name, user_mail, user_pass))
        user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    else:
        user_id = user['user_id']

    purchase_total = card['card_price'] * card_amount

    conn.execute('INSERT INTO Purchase (user_id, card_id, card_amount, purchase_total) VALUES (?, ?, ?, ?)', 
                 (user_id, card_id, card_amount, purchase_total))
    conn.commit()
    conn.close()
    return render_template('payment_success.html')

# Ruta para ver detalles de una carta
@app.route('/card/<int:card_id>', methods=['GET'])
def view_card(card_id):
    conn = get_db_connection()
    card = conn.execute('SELECT * FROM Card WHERE card_id = ?', (card_id,)).fetchone()
    conn.close()
    if card is None:
        return "Card not found", 404
    return render_template('view_card.html', card=card)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)