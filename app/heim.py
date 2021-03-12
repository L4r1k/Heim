from flask import Flask, render_template, jsonify, request, redirect, url_for, abort, session
from flask_jwt_extended import create_access_token, get_jwt_identity, get_unverified_jwt_headers, jwt_required, JWTManager 
import random
import requests

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '629cc538-2d80-4bf8-87f6-7ccde1c70e2e'
app.config['JWT_SECRET_KEY'] = 'arottenbranchwillbefoundineverytree'
jwt = JWTManager(app)

FLAG = 'flag{liveheim_laughheim_loveheim}'
error_prompts = [
    'The forest is moving',
    'The ground is shaking',
    'A foul smell from the swamp',
    'A cold wind blows from the mountains'
]

# Home Page
# Supports GET requests
# If authorized user is redirected to /heim where they are presented with JSON containing base64 encoded API schema
# If unauthorized, user is presented with index.html template containing input form prompting for a username that results in POST to /auth
@app.route('/', methods=['GET'])
@jwt_required(optional=True)
def index():
    if get_jwt_identity():
        return redirect('/heim', 302)
    else:
        return render_template('index.html'), 200

# Auth Page
# Supports GET and POST requests
# GET: Silly middleman method that exists to leak the jwt_secret_key. Just takes the passed access_token and redirects to /auth/authorized with it to return it to the user
# POST: Post method that generates the access_key. Posted to by form on home page. Creates access_token, then redirects to GET /auth to leak the jwt_secret_key 
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        access_token = request.args.get('access_token')
        if access_token:
            session['access_token'] = access_token
            return redirect('/auth/authorized', 302)
        else:
            abort(404) 
    elif request.method == 'POST':
        username = request.form['username']
        if username == 'odin':
            return jsonify(error='You are not wise enough to be Odin'), 401 
        else:
            access_token = create_access_token(identity=username)
            return redirect(url_for('.auth', access_token=access_token, jwt_secret_key=app.config['JWT_SECRET_KEY']), 302)

# Authorized Page
# Supports GET requests
# /auth redirects here upon successful access_token generation. This method takes the access_token from the session and returns it in JSON to the user 
@app.route('/auth/authorized', methods=['GET'])
def authorized():
    access_token = session['access_token']
    if access_token:
        return jsonify(access_token=access_token), 200
    else:
        abort(404)

# Heim Page
# Supports GET requests
# Homepage redirects here when a user sends an authenticated GET request to it. This page returns the base64 encoded API schema to the user
@app.route('/heim', methods=['GET'])
@jwt_required()
def heim():
    return jsonify({
        'msg': 'ewogICAgImFwaSI6IHsKICAgICAgICAidjEiOiB7CiAgICAgICAgICAgICIvYXV0aCI6IHsKICAgICAgICAgICAgICAgICJnZXQiOiB7CiAgICAgICAgICAgICAgICAgICAgInN1bW1hcnkiOiAiRGVidWdnaW5nIG1ldGhvZCBmb3IgYXV0aG9yaXphdGlvbiBwb3N0IiwKICAgICAgICAgICAgICAgICAgICAic2VjdXJpdHkiOiAiTm9uZSIsCiAgICAgICAgICAgICAgICAgICAgInBhcmFtZXRlcnMiOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICJhY2Nlc3NfdG9rZW4iOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiB0cnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIkFjY2VzcyB0b2tlbiBmcm9tIHJlY2VudGx5IGF1dGhvcml6ZWQgVmlraW5nIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJpbiI6ICJwYXRoIiwKICAgICAgICAgICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICAgICAgICAgImp3dF9zZWNyZXRfa2V5IjogewogICAgICAgICAgICAgICAgICAgICAgICAgICAgInJlcXVpcmVkIjogZmFsc2UsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiRGVidWdnaW5nIC0gc2hvdWxkIGJlIHJlbW92ZWQgaW4gcHJvZCBIZWltIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJpbiI6ICJwYXRoIgogICAgICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICJwb3N0IjogewogICAgICAgICAgICAgICAgICAgICJzdW1tYXJ5IjogIkF1dGhvcml6ZSB5b3Vyc2VsZiBhcyBhIFZpa2luZyIsCiAgICAgICAgICAgICAgICAgICAgInNlY3VyaXR5IjogIk5vbmUiLAogICAgICAgICAgICAgICAgICAgICJwYXJhbWV0ZXJzIjogewogICAgICAgICAgICAgICAgICAgICAgICAidXNlcm5hbWUiOiB7CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiB0cnVlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIllvdXIgVmlraW5nIG5hbWUiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImluIjogImJvZHkiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImNvbnRlbnQiOiAibXVsdGlwYXJ0L3gtd3d3LWZvcm0tdXJsZW5jb2RlZCIKICAgICAgICAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfSwKICAgICAgICAgICAgIi9oZWltIjogewogICAgICAgICAgICAgICAgImdldCI6IHsKICAgICAgICAgICAgICAgICAgICAic3VtbWFyeSI6ICJMaXN0IHRoZSBlbmRwb2ludHMgYXZhaWxhYmxlIHRvIG5hbWVkIFZpa2luZ3MiLAogICAgICAgICAgICAgICAgICAgICJzZWN1cml0eSI6ICJCZWFyZXJBdXRoIgogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9LAogICAgICAgICAgICAiL2ZsYWciOiB7CiAgICAgICAgICAgICAgICAiZ2V0IjogewogICAgICAgICAgICAgICAgICAgICJzdW1tYXJ5IjogIlJldHJpZXZlIHRoZSBmbGFnIiwKICAgICAgICAgICAgICAgICAgICAic2VjdXJpdHkiOiAiQmVhcmVyQXV0aCIKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfQogICAgICAgIH0KICAgIH0KfQ=='
        }), 200

# Flag Page
# Supports GET requests
# If the user is authenticated as Odin, returns the flag in JSON. Otherwise returns an error message with a hint
@app.route('/flag', methods=['GET'])
@jwt_required()
def flag():
    current_user = get_jwt_identity()
    if current_user.lower() == 'odin':
        return jsonify(flag=FLAG), 200
    else:
        return jsonify(msg='You are not worthy. Only the AllFather Odin may view the flag'), 401 

@app.errorhandler(404)
def page_not_found(e):
    return  render_template('404.html', error_header=random.choice(error_prompts), error=e), 404

if __name__=="__main__":
    app.run()
