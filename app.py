import sqlite3
from flask import Flask, request, session, g, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = "very_insecure_key_for_demo"
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codename TEXT UNIQUE,
            secret_code TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS missions(
            mission_id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER,
            mission_content TEXT
        );
    ''')
    conn.commit()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        codename = request.form.get('codename')
        secret_code = request.form.get('secret_code')

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO agents (codename, secret_code) VALUES (?, ?)",
                           (codename, secret_code))
            conn.commit()
            return render_template('register.html', message="Registration successful! You can now login.")
        except sqlite3.IntegrityError:
            return render_template('register.html', message="Codename already exists. Try a different one.")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        codename = request.form.get('codename')
        secret_code = request.form.get('secret_code')

        conn = get_db()
        cursor = conn.cursor()

        query = f"SELECT id, codename FROM agents WHERE codename='{codename}' AND secret_code='{secret_code}'"
        cursor.execute(query)
        agent = cursor.fetchone()

        if agent:
            session['agent_id'] = agent[0]
            session['codename'] = agent[1]
            return redirect(url_for('missions'))
        else:
            return render_template('login.html', message="Login failed! Check your credentials.")
    return render_template('login.html')


@app.route('/missions')
def missions():
    if 'agent_id' not in session:
        return redirect(url_for('login'))

    agent_id = session['agent_id']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT mission_id, mission_content FROM missions WHERE agent_id=?", (agent_id,))
    agent_missions = cursor.fetchall()

    return render_template('missions.html', missions=agent_missions)


@app.route('/add_mission', methods=['POST'])
def add_mission():
    if 'agent_id' not in session:
        return redirect(url_for('login'))

    content = request.form.get('mission_content')
    agent_id = session['agent_id']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO missions (agent_id, mission_content) VALUES (?, ?)", (agent_id, content))
    conn.commit()

    return redirect(url_for('missions'))

@app.route('/mission/<int:mission_id>')
def view_mission(mission_id):

    if 'agent_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT mission_content, agent_id FROM missions WHERE mission_id=?", (mission_id,))
    row = cursor.fetchone()

    if row:
        mission_text = row[0]
        owner_id = row[1]
        return render_template('mission.html', mission_id=mission_id, mission_text=mission_text, owner_id=owner_id)
    else:
        return "Mission not found!"


@app.route('/search', methods=['GET', 'POST'])
def search_missions():
    if 'agent_id' not in session:
        return "Access denied. Please <a href='/login'>login</a> first."

    if request.method == 'POST':
        keyword = request.form.get('keyword')

        conn = get_db()
        cursor = conn.cursor()

        query = f"SELECT mission_id, mission_content FROM missions WHERE mission_content LIKE '%{keyword}%'"
        cursor.execute(query)

        results = cursor.fetchall()

        return render_template('search.html', results=results)
    else:

        return render_template('search.html', results=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
