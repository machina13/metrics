from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# Configuración de la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        dbname='data',
        user='myuser',
        password='mypassword',
        host='127.0.0.1',
        port='5432'
    )
    return conn

def get_generation_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT generation from server')
    generation = cursor.fetchall()
    cursor.close()
    conn.close()
    return generation

@app.route('/')
def index():
    generation = get_generation_data()
    return render_template('form.html', generation=generation)

@app.route('/get_servers', methods=['POST'])
def get_servers():
    generation = request.form['generation']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT name FROM server WHERE generation = %s ', (generation,))
    servers = cursor.fetchall()
    conn.close()
    return jsonify(servers)

@app.route('/get_cores', methods=['POST'])
def get_cores():
    server = request.form['server']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT cores FROM server WHERE name = %s', (server,))
    cores = cursor.fetchall()
    conn.close()
    return jsonify(cores)

@app.route('/get_smt', methods=['POST'])
def get_smt():
    cores = request.form['cores']
    server = request.form['server']
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT DISTINCT b.s, b.smt2, b.smt4, b.smt8
        FROM server AS a
        JOIN rPerf AS b ON a.id_server = b.id_server
        WHERE a.cores = %s AND a.name = %s
    """
    cursor.execute(query, (cores, server))
    result = cursor.fetchall()

    conn.close()

    smt_data = [{"sm": row[0], "smt2": row[1], "smt4": row[2], "smt8": row[3]} for row in result]
    return jsonify(smt_data)

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/add_configurations', methods=['POST'])
def add_configurations():
    configurations = request.json.get('configurations')
    conn = get_db_connection()
    cursor = conn.cursor()
    for config in configurations:
        cursor.execute(
            'INSERT INTO configurations (generation, server, cores, sm, smt2, smt4, smt8) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (config['generation'], config['server'], config['cores'], config['sm'], config['smt2'], config['smt4'], config['smt8'])
        )
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
