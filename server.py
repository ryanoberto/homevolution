# all the imports
import sqlite3
import os.path
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from homevolution.db import init_db
from flask_cors import CORS
from contextlib import closing
from homevolution.device import action, get_devices, list_devices
import homevolution.zoneminder as zoneminder
import homevolution.kodi as kodi
import homevolution.schedules as sched
import homevolution.kodiapi as kodiapi
#import homevolution.modules as modules


# configuration
DATABASE = 'homevolution.db'
DEBUG = True
SECRET_KEY = 'DeeXPDogs5svAQ7giGwaGgpYA154jFfxoqRw'
USERNAME = 'admin'
PASSWORD = 'admin'

# create our little application :)
app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('database.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

"""
Check to see if there is a database else create on
"""
if not os.path.exists("homevolution.db"):
        init_db()


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		templateData={}
		return render_template('index.html', **templateData)


@app.route('/kodi')
def kodis():
   # Pass the template data into the template dashboard.html and return it to the user
                
	if not session.get('logged_in'):
                flash('Need to login')
                return render_template('login.html')
        else:
		updated_nowplaying = kodi.nowplaying(True)
                templateData = {
		 'kodi' : kodi.list(),
                'now_playing' : updated_nowplaying['now_playing'],
                'now_playing_image' : updated_nowplaying['now_playing_image'],
                }

                return render_template('kodi.html', **templateData)

@app.route('/schedules')
def schedules():
   # Pass the template data into the template dashboard.html and return it to the user
                update_schedule = sched.gettime("sname")
		update_run = sched.getrun("sname")
                #SCHEDULE_TIME = config['SCHEDULE']
                templateData = {
                'schedule' : sched.SCHEDULE,
                'schedules' : update_schedule,
                'schedulerun' : update_run,
                }

                return render_template('schedules.html', **templateData)


@app.route('/devices')
def show_devices():
	if not session.get('logged_in'):
		flash('Need to login')
		return render_template('login.html')
	else:
		get_device = get_devices()
		for result in get_device.itervalues():
			if "error" in str(result):
				error = get_devices()
			else:
				error = None
        	templateData={ 
		'error' : error,
		'devices' : get_devices()
		}
        	return render_template('devices.html', **templateData)


@app.route('/<action>/<module>',methods=['POST'])
def add(action, module):
	if not session.get('logged_in'):
        	abort(401)
	if action == "add":
                if module == "device":
			g.db.execute('insert into slaves (node, key) values (?, ?)',
                 		[request.form['node'], request.form['key']])
    			g.db.commit()
    			flash('New device was successfully added')
		
		if module == "kodi":
                        g.db.execute('insert into kodi (name, port) values (?,?)',
                                [request.form['name'], request.form['port']])
                        g.db.commit()
                        flash('New server was successfully added')	
		
		if module == "zoneminder":
                        g.db.execute('insert into zoneminder (name, url, port) values (?, ?, ?)',
                                [request.form['name'], request.form['url'], request.form['port']])
                        g.db.commit()
                        flash('New server was successfully added')
	
	elif action == "del":
		if module == "device":
                        g.db.execute('delete from slaves where node=?',
                                [request.form['node']])
                        g.db.commit()
                        flash('Device was deleted')

                if module == "kodi":
                        g.db.execute('delete from kodi where name=?',
                                [request.form['name']])
                        g.db.commit()
                        flash('Server was deleted')

                if module == "zoneminder":
                        g.db.execute('delete from zoneminder where name=?',
                                [request.form['name']])
                        g.db.commit()
                        flash('Server was deleted')

	
	return redirect(url_for('settings'))


@app.route('/dashboard')
def dashboards():
        templateData={ }
        return render_template('dashboard.html', **templateData)

#@app.route('/add/modules', methods=['POST'])
#def add_module():
#    if not session.get('logged_in'):
#        abort(401)
#    g.db.execute('insert into modules (name, url, enabled) values (?, ?, ?)',
#                 [request.form['name'], request.form['url'], request.form['enabled']])
#    g.db.commit()
#    flash('New module was successfully added')
#    return redirect(url_for('settings'))


@app.route('/show')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

# Settings Stuff add edit and delete
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into slaves (node, key) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/cameras')
def cameras():
   # Pass the template data into the template dashboard.html and return it to the user
	if not session.get('logged_in'):
                flash('Need to login')
                return render_template('login.html')
        else:
                if "error" in str(zoneminder.get_cameras()):
                	error = zoneminder.get_cameras()
                else:
                        error = None

		templateData = {
		'error' : error,
		'zmhost' : zoneminder.ZMHOST,
		'zoneminder' : zoneminder.get_cameras(),
		}

	return render_template('cameras.html', **templateData)


@app.route('/settings',methods=['GET','POST'])
def settings():
   # Pass the template data into the template dashboard.html and return it to the user
	if not session.get('logged_in'):
                flash('Need to login')
                return render_template('login.html')
        else:

		templateData = {
		'nodes' : list_devices(),
		'kodi' : kodi.list(),
		'zoneminder' : zoneminder.list(),
		'devices' : get_devices()
		}
		return render_template('settings.html', **templateData)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


#API stuff

@app.route('/api/<plugin>/<action>', methods = ['GET'])
def service(plugin, action):
        if plugin == "kodi":
                if action == "options":
                        return jsonify(KODI_API_OPT)
                if action == "playing":
                        updated_nowplaying = thing(KODI)
                        return jsonify( { 'now_playing': updated_nowplaying['now_playing'] } )
                if action == "play":
                        return "play"
                if action == "stop":
                        return "stop"
                if action == "rewind":
                        return "rewind"
                if action == "begining":
                        return "begining"
                if action == "fastforward":
                        return "fastforward"
                if action == "end":
                        return "end"
                if action == "volup":
                        return "volup"
                if action == "voldwn":
                        return "voldwn"
                if action == "info":
                        return "info"

                else:
                        return abort(404)
        else:

                return abort(404)



if __name__ == '__main__':
    app.run(
	debug=True,
	host="0.0.0.0",
        port=int("80")
)


