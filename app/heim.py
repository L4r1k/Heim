from flask import Flask, render_template, jsonify, request, redirect, url_for, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, get_unverified_jwt_headers, jwt_required, JWTManager 
import random
import requests

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['JWT_SECRET_KEY'] = 'arottenbranchwillbefoundineverytree'
jwt = JWTManager(app)

FLAG = 'flag{liveheim_laughheim_loveheim}'
error_prompts = [
    'The forest is moving',
    'The ground is shaking',
    'A foul smell from the swamp',
    'A cold wind blows from the mountains'
]

@app.route('/')
@jwt_required(optional=True)
def index():
    if get_jwt_identity():
        return redirect('/heim', 302)
    else:
        return render_template('index.html')

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    if username == 'odin':
        return jsonify(error='You are not wise enough to be Odin')
    else:
        access_token = create_access_token(identity=username)

        return redirect(url_for('.auth', access_token=access_token, jwt_secret_key=app.config['JWT_SECRET_KEY']), 302)

@app.route('/auth', methods=['GET'])
def get_token():
    access_token = request.args.get('access_token')
    if access_token:
        return jsonify(access_token=access_token)
    else:
        abort(404) 

@app.route('/heim', methods=['GET'])
@jwt_required()
def heim():
    return jsonify({
        'msg': 'ewogICAgImFwaSI6IHsKICAgICAgICAidjEiOiB7CiAgICAgICAgICAgICIvYXV0aCI6IHsKICAgICAgICAgICAgICAgICJwb3N0IjogewogICAgICAgICAgICAgICAgICAgICJzdW1tYXJ5IjogIkF1dGhvcml6ZSB5b3Vyc2VsZiBhcyBhIFZpa2luZyIsCiAgICAgICAgICAgICAgICAgICAgInNlY3VyaXR5IjogIk5vbmUiLAogICAgICAgICAgICAgICAgICAgICJwYXJhbWV0ZXJzIjogewogICAgICAgICAgICAgICAgICAgICAgICAibmFtZSI6ICJ1c2VybmFtZSIsCiAgICAgICAgICAgICAgICAgICAgICAgICJyZXF1aXJlZCI6IHRydWUsCiAgICAgICAgICAgICAgICAgICAgICAgICJkZXNjcmlwdGlvbiI6ICJZb3VyIFZpa2luZyBuYW1lIiwKICAgICAgICAgICAgICAgICAgICAgICAgImluIjogImJvZHkiLAogICAgICAgICAgICAgICAgICAgICAgICAiY29udGVudCI6ICJtdWx0aXBhcnQveC13d3ctZm9ybS11cmxlbmNvZGVkIgogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfSwKICAgICAgICAgICAgIi9oZWltIjogewogICAgICAgICAgICAgICAgImdldCI6IHsKICAgICAgICAgICAgICAgICAgICAic3VtbWFyeSI6ICJMaXN0IHRoZSBlbmRwb2ludHMgYXZhaWxhYmxlIHRvIG5hbWVkIFZpa2luZ3MiLAogICAgICAgICAgICAgICAgICAgICJzZWN1cml0eSI6ICJCZWFyZXJBdXRoIgogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9LAogICAgICAgICAgICAiL2ZsYWciOiB7CiAgICAgICAgICAgICAgICAiZ2V0IjogewogICAgICAgICAgICAgICAgICAgICJzdW1tYXJ5IjogIlJldHJpZXZlIHRoZSBmbGFnIiwKICAgICAgICAgICAgICAgICAgICAic2VjdXJpdHkiOiAiQmVhcmVyQXV0aCIKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfQogICAgICAgIH0KICAgIH0KfQ=='
        }), 200

@app.route('/flag', methods=['GET'])
@jwt_required()
def flag():
    current_user = get_jwt_identity()
    if current_user.lower() == 'odin':
        return jsonify(flag=FLAG), 200
    else:
        return jsonify(msg=f'You are not worthy. Only the AllFather may view the flag'), 401 

@app.errorhandler(404)
def page_not_found(e):
    return  render_template('404.html', error_header=random.choice(error_prompts), error=e)

if __name__=="__main__":
    app.run()
