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
    cursor.execute('SELECT DISTINCT generation FROM server')
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
    cursor.execute('SELECT DISTINCT name FROM server WHERE generation = %s', (generation,))
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

@app.route('/get_metric_data', methods=['POST'])
def get_metric_data():
    metric = request.form['metric']
    cores = request.form['cores']
    server = request.form['server']
    conn = get_db_connection()
    cursor = conn.cursor()

    metric_query = {
        'rperf': """
            SELECT st, smt2, smt4, smt8, clock, model, type, socket_count, core_per_socket
            FROM rperf
            WHERE id_server = (SELECT id_server FROM server WHERE name = %s AND cores = %s)
        """,
        'saps': """
            SELECT sd_bench_saps, hana_prod_saps, clock, model, type, socket_count, core_per_socket
            FROM saps
            WHERE id_server = (SELECT id_server FROM server WHERE name = %s AND cores = %s)
        """,
        'spec': """
            SELECT specrate2017_int_peak, specrate2017_int_basek, clock, model, type, socket_count, core_per_socket
            FROM spec
            WHERE id_server = (SELECT id_server FROM server WHERE name = %s AND cores = %s)
        """,
        'cpw': """
            SELECT cpw, clock, model, type, socket_count, core_per_socket
            FROM cpw
            WHERE id_server = (SELECT id_server FROM server WHERE name = %s AND cores = %s)
        """
    }

    query = metric_query[metric]
    cursor.execute(query, (server, cores,))
    result = cursor.fetchall()
    conn.close()

    metric_data = []
    if metric == 'rperf':
        metric_data = [{"st": row[0], "smt2": row[1], "smt4": row[2], "smt8": row[3],
                        "clock": row[4], "model": row[5], "type": row[6],
                        "socket_count": row[7], "core_per_socket": row[8]} for row in result]
    elif metric == 'saps':
        metric_data = [{"sd_bench_saps": row[0], "hana_prod_saps": row[1],
                        "clock": row[2], "model": row[3], "type": row[4],
                        "socket_count": row[5], "core_per_socket": row[6]} for row in result]
    elif metric == 'spec':
        metric_data = [{"specrate2017_int_peak": row[0], "specrate2017_int_basek": row[1],
                        "clock": row[2], "model": row[3], "type": row[4],
                        "socket_count": row[5], "core_per_socket": row[6]} for row in result]
    elif metric == 'cpw':
        metric_data = [{"cpw": row[0],
                        "clock": row[1], "model": row[2], "type": row[3],
                        "socket_count": row[4], "core_per_socket": row[5]} for row in result]

    return jsonify(metric_data)

@app.route('/save_configurations', methods=['POST'])
def save_configurations():
    configurations = request.json.get('configurations')
    conn = get_db_connection()
    cursor = conn.cursor()

    for config in configurations:
        if 'st' in config:
            cursor.execute(
                'INSERT INTO configurations (generation, server, cores, st, smt2, smt4, smt8, clock, model, type, socket_count, core_per_socket, percentage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (config['generation'], config['server'], config['cores'], config['st'], config['smt2'], config['smt4'], config['smt8'], config['clock'], config['model'], config['type'], config['socket_count'], config['core_per_socket'], config['percentage'])
            )
        elif 'sd_bench_saps' in config:
            cursor.execute(
                'INSERT INTO configurations (generation, server, cores, sd_bench_saps, hana_prod_saps, clock, model, type, socket_count, core_per_socket, percentage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (config['generation'], config['server'], config['cores'], config['sd_bench_saps'], config['hana_prod_saps'], config['clock'], config['model'], config['type'], config['socket_count'], config['core_per_socket'], config['percentage'])
            )
        elif 'specrate2017_int_peak' in config:
            cursor.execute(
                'INSERT INTO configurations (generation, server, cores, specrate2017_int_peak, specrate2017_int_basek, clock, model, type, socket_count, core_per_socket, percentage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (config['generation'], config['server'], config['cores'], config['specrate2017_int_peak'], config['specrate2017_int_basek'], config['clock'], config['model'], config['type'], config['socket_count'], config['core_per_socket'], config['percentage'])
            )
        elif 'cpw' in config:
            cursor.execute(
                'INSERT INTO configurations (generation, server, cores, cpw, clock, model, type, socket_count, core_per_socket, percentage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (config['generation'], config['server'], config['cores'], config['cpw'], config['clock'], config['model'], config['type'], config['socket_count'], config['core_per_socket'], config['percentage'])
            )

    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
