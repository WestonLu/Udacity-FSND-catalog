from flask import  render_template, request, redirect,  \
    url_for, flash
from flask import session as login_session
import random
import string
import httplib2
import json
from flask import make_response
from user import *

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/login')
def showLogin():
    if 'username' in login_session:
        return redirect(url_for('showShops'))
    else:
        # Create anti-forgery state token
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in xrange(32))
        login_session['state'] = state
        url = "https://github.com/login/oauth/authorize?client_id" \
              "=4b45d6b548788b9b9033&state=%s" % (state)
        return redirect(url)


@app.route('/ghconnect', methods=['POST'])
def ghconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_code = request.data
    print "access code received %s " % access_code
    # Use code to get token from API
    app_id = "4b45d6b548788b9b9033"
    app_secret = "797b32b9519a7b523e1dbea081173d2cda63002f"
    url = 'https://github.com/login/oauth/access_token?client_id=%s' \
          '&client_secret=%s&code=%s' % (
              app_id, app_secret, access_code)
    h = httplib2.Http()
    result = h.request(url, 'POST', headers={
        'Accept': 'application/json'})[1]
    token = json.loads(result)['access_token']
    # Use token to get user info from API
    url = "https://api.github.com/user?access_token=%s" % (token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'github'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['github_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout
    login_session['access_token'] = token

    # # Get user picture
    login_session['picture'] = data["avatar_url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    # show message on the welcome page
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: ' \
              '150px;-webkit-border-radius: 150px;-moz-border-radius: ' \
              '150px;"> '
    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/ghdisconnect')
def ghdisconnect():
    return "you have been logged out"


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'github':
            ghdisconnect()
            del login_session['github_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showHomepage'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showHomepage'))