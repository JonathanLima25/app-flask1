import db
from converters import RegexConverter
from flask import Flask, abort, url_for

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

@app.route('/')
def index():
    html = ['<ul>']
    for username, user in db.users.items():
        html.append(
            f"<li><a href='{url_for('user', username=username)}'>{user['name']}</a></li>"
        )
    html.append('</ul>')
    return '\n'.join(html)

def profile(username):
    user = db.users.get(username)

    if user:
        return f"""
            <h1>{user['name']}</h1>
            <img src="{user['image']}"/><br>
            telefone: {user['tel']} <br>
            <a href="/">Voltar</a>
        """
    else:
        return abort(404, "User not found")

app.add_url_rule('/user/<username>/', view_func=profile, endpoint='user')

@app.route('/user/<username>/<int:quote_id>')
def quote(username, quote_id):
    user = db.users.get(username, {})
    quote = user.get("quotes").get(quote_id)
    if user and quote:
        return f"""
            <h1>{user['name']}</h1>
            <img src="{user['image']}"/><br>
            <p><q>{quote}</q></p>
        """
    else:
        return abort(404, "Quote not found")
        
@app.route('/file/<path:filename>/')
def filepath(filename):
    return f"argumento recebido: {filename}"

@app.route('/reg/<regex("a.*"):name>/')
def reg(name):
    return f"Argumentos iniciados com a letra a: {name}"

app.run(use_reloader=True)