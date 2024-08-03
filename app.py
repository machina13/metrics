
from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# Configuración de la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        dbname='data',
        user='myuser',
        password='mypassword',
        host='db',
        port='5432'
    )
    return conn

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/get_servers', methods=['POST'])
def get_servers():
    generation = request.form['generation']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT name from server', (generation,))
    servers = cursor.fetchall()
    conn.close()
    return jsonify(servers)

@app.route('/get_cores', methods=['POST'])
def get_cores():
    server = request.form['server']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT cores FROM configurations WHERE server = %s', (server,))
    cores = cursor.fetchall()
    conn.close()
    return jsonify(cores)

@app.route('/get_smt', methods=['POST'])
def get_smt():
    cores = request.form['cores']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT smt FROM configurations WHERE cores = %s', (cores,))
    smts = cursor.fetchall()
    conn.close()
    return jsonify(smts)

@app.route('/get_rperf', methods=['POST'])
def get_rperf():
    smt = request.form['smt']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT rperf FROM configurations WHERE smt = %s', (smt,))
    rperfs = cursor.fetchall()
    conn.close()
    return jsonify(rperfs)

@app.route('/add_configuration', methods=['POST'])
def add_configuration():
    generation = request.form['generation']
    server = request.form['server']
    cores = request.form['cores']
    smt = request.form['smt']
    rperf = request.form['rperf']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO configurations (generation, server, cores, smt, rperf) VALUES (%s, %s, %s, %s, %s)',
        (generation, server, cores, smt, rperf)
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/get_configurations', methods=['GET'])
def get_configurations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT generation, server, cores, smt, rperf FROM configurations')
    configurations = cursor.fetchall()
    conn.close()
    return jsonify(configurations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

