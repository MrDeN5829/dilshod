from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Hardcoded RDS credentials (avoid this in production)
DB_HOST = '<your-rds-endpoint>'
DB_PORT = '5432'
DB_NAME = 'db_<first_name>'
DB_USER = 'postgres'
DB_PASSWORD = '<your_password>'

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode='require'
    )

@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tbl_<change>_data;") #change
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in rows]
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tbl_<first_name>_data;") # change
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in rows]
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add', methods=['POST'])
def add_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tbl_<first_name>_data (class) VALUES (%s)", # change
        ('TEST',)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'ok'}), 201

@app.route('/delete', methods=['POST'])
def delete():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM tbl_<first_name>_data WHERE id = (SELECT MAX(id) FROM tbl_<first_name>_data)" #change
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
