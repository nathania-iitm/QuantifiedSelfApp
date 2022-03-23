from flask import Flask
from flask import render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.sqlite3'

db = SQLAlchemy(app)



class tracker(db.Model):
  __tablename__ = 'tracker'
  tracker_name = db.Column(db.String , primary_key =True, nullable = False, unique = True)
  description = db.Column(db.String ,unique = False, nullable = False )
  tracker_type = db.Column(db.String, unique = False, nullable = False )
  time =db.Column(db.String, unique = False, nullable = False )
  user_id = db.Column(db.Integer ,unique = False, nullable = True )
  tracker_value= db.Column(db.String, unique = False, nullable = True)

class log(db.Model):
  __tablename__ = 'log'
  sr_no = db.Column(db.Integer ,primary_key =True, unique = False, nullable = False, autoincrement=True)
  tracker_log = db.Column(db.String ,unique = False, nullable = False )
  time = db.Column(db.String,  unique = False, nullable = True )
  value =db.Column(db.String, unique = False, nullable = True )
  note = db.Column(db.String,  unique = False, nullable = True )



@app.route('/', methods=["GET", "POST"])
def home():
  if request.method == "POST":
    return redirect('/dash')
  return render_template('home.html')



@app.route('/dash', methods=["GET","POST"])
def dashboard():
  data = tracker.query.with_entities(tracker.tracker_name,tracker.description,tracker.tracker_type,tracker.time,tracker.user_id,tracker.tracker_value).all()
  n = len(data)
  return render_template('dash.html',data=data ,n=n)



@app.route('/create', methods=["GET", "POST"])
def create():
  if request.method == "POST":
    trackers = request.form['tracker']
    disc = request.form['disc']
    type= request.form['type']
    val=request.form['val']
    notes=request.form['notes']
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S.%f')

    a = tracker(tracker_name=trackers, description=disc, tracker_type=type,time=ind_time[:19],tracker_value=val)
    b= log(tracker_log=trackers, time=ind_time[:19], value=val, note=notes)
    db.session.add(a)
    db.session.add(b)
    db.session.commit()
  
    return redirect('/dash')
  return render_template('create.html')


@app.route('/editTracker/<id>', methods=["GET", "POST"])
def editTracker(id):
  data = tracker.query.with_entities(tracker.tracker_name,tracker.description,tracker.tracker_type,tracker.time,tracker.user_id,tracker.tracker_value).all()

  for i in data:
    if i[0] == id:
      row = i
  if request.method == "POST":
    my_data = tracker.query.get(id)
    my_data.tracker_name = request.form['tracker']
    my_data.description = request.form['disc']
    my_data.tracker_type = request.form['type']
    my_data.time = request.form['tim']

    db.session.commit()
    return redirect('/dash')
  return render_template('edit_t.html', row=row)



@app.route('/deleteTracker/<id>')
def delCard(id):
  my_data = tracker.query.get(id)
  db.session.delete(my_data)
  db.session.commit()
  return redirect('/dash')



@app.route('/view/<id>', methods=["GET", "POST"])
def view(id):
  logdata = log.query.with_entities(log.sr_no,log.tracker_log,log.time,log.value,log.note).all()
  z = 0
  l=[]
  x_axis=[]
  y_axis=[]
  for j in logdata:
    if j[1] == id: #tracker==tracker
      z+=1 #keeps count of number of logs
      row = j 
      q=[]
      for p in j:
        q.append(p)
      l.append(q)
      d=j[2]
      x_axis.append(d[:5])
      y_axis.append(j[3])


  plt.clf()
  plt.figure(facecolor='lavender')
  plt.rcParams["font.family"] = "Georgia"
  plt.plot(x_axis, y_axis, 'o', color='Teal')
  
  plt.xticks(rotation = 75)
  fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(7, 5)
  url_for('static',filename='myplot.png')
  plt.savefig('static/myplot.png')
           
  return render_template('viewlog.html', row=row, l=l, z=z)



@app.route('/addlog/<string:id>', methods=["GET", "POST"])
def addlog(id):
  data = tracker.query.with_entities(tracker.tracker_name,tracker.description,tracker.tracker_type,tracker.time,tracker.user_id,tracker.tracker_value).all()
  
  if request.method == "POST":
    logs=request.form['opt']
    val = request.form['val']
    notes = request.form['notes']
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %H:%M:%S.%f')


    b = log(tracker_log=logs, time=ind_time[:19], value=val, note=notes)
    
    db.session.add(b)
    db.session.commit()
    url_to_be_redirected="/view/"+str(id)
    return redirect(url_to_be_redirected)
  return render_template('addlog.html',id=id, data=data)



@app.route('/editLog/<string:sr_no>', methods=["GET", "POST"])
def editLog(sr_no):
  logdata = log.query.with_entities(log.sr_no,log.tracker_log,log.time,log.value,log.note).all()
  
  log_row=[]
  for p in logdata:
    if str(p[0]) == str(sr_no):
      log_row = p
      sr_no=sr_no
      break

  if request.method == "POST":
    my_data = log.query.get(sr_no)
    my_data.tracker_log = request.form['opt']
    my_data.value = request.form['val']
    my_data.note = request.form['notes']
    my_data.time = request.form['tim']

    my_dash=log.query.get(sr_no)
    my_dash.time=request.form['tim']
    db.session.commit()
    url_to_be_redirected1= '/view/'+str(log_row[1])
    return redirect(url_to_be_redirected1)
  return render_template('edit_l.html', sr_no=sr_no,log_row=log_row)



@app.route('/deleteLog/<string:id>')
def deleteLog(id):
  logdata = log.query.with_entities(log.sr_no,log.tracker_log,log.time,log.value,log.note).all()
  for i in logdata:
    if str(i[0])==str(id):
      p=i[1]
      break
  my_data = log.query.get(id)
  db.session.delete(my_data)
  db.session.commit()
  url_to_be_redirected="/view/"+str(p)
  return redirect(url_to_be_redirected)



if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')