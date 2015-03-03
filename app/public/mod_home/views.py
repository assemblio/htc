from flask import request, g, url_for, render_template

def index():
    if request.method == 'POST':
        username = request.form['username']
        if username in g.users:
            # Authenticate and log in!
            if g.users[username].authenticate(request.form['password']):
                return '''
                        <a href="{0}">View users</a><br/>
                        <a href="{1}">Create users</a><br/>
                        <a href="{2}">Logout</a>
                        '''.format(url_for('user_view'),
                                   url_for('user_create'),
                                   url_for('logout'),)
        return 'Failure :('

    return render_template('index.html')