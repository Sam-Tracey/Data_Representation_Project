from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mail import Mail, Message
import json
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from dataDAO import dataDAO

app = Flask(__name__)
mail = Mail(app)

'''
# Email configuration
# For obvious reasons I am not going to include my email and password here.
# This would allow the "forgotten password" feature to work.

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
'''


app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key='dataRepresentation'

@app.route('/')
def index():
    return render_template('login.html')

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # search for user in database
        dataDAO.login(username, password)
        if dataDAO.login(username, password) is not None:
            session['username'] = username
            return render_template('home.html')
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

# Route for signing up a new user
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # get the form data
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        # insert user into database
        dataDAO.insertUser(username, password, email)
        return redirect(url_for('index'))
    return render_template('signup.html')

# I've included this route for the "forgotten password" feature but not using it in the app.
@app.route('/forgotpass', methods=['GET', 'POST'])
def forgotpass():
    if request.method == 'POST':
        # get the form data
        email = request.form['email']
        # username = request.form['username']

        user = dataDAO.findUserByEmail(email)

        # send the password reset email if the user was found
        if user:
            msg = Message('Password Reset', sender='your_email@example.com', recipients=[email])
            msg.body = 'Your password is: ' + user['password']
            mail.send(msg)
        else:
            # display an error message if the user was not found
            flash('User not found')

        return redirect(url_for('index'))
    return render_template('forgotpass.html')

    
# Home page route
@app.route('/home')
def home():
    if not 'username' in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# About Page route.
@app.route('/about')
def about():
    if not 'username' in session:
        return redirect(url_for('login'))
    return render_template('about.html')

# Employee page route
@app.route('/employee')
def employee():
    if not 'username' in session:
        return redirect(url_for('login'))
    return render_template('employee.html')
    
# Route for reading the data from the local attrition rate data from database
@app.route('/get_data')
def employee_api():
    if not 'username' in session:
        return redirect(url_for('login'))
    results = dataDAO.readQuits()
    return jsonify(results)

# Reading all data to MySQL on successful login
@app.route('/load_data', methods=['GET'])
def load_local_data():
    if not 'username' in session:
        return redirect(url_for('login'))
    dataDAO.loadLocalQuits()
    dataDAO.loadOpenings()
    dataDAO.loadMFGEMP()
    dataDAO.loadUnemployment()
    dataDAO.loadQuits()

    return jsonify({'message': 'Data loaded from local file'})
    
# Find local quit data by ID
@app.route('/employee/<int:id>')
def findById(id):
    if not 'username' in session:
        return redirect(url_for('login'))
    results = dataDAO.findQuitsByID(id)
    return jsonify(results)

# Route for creating new emplyee quit entry from form
@app.route('/employee', methods=['POST'])
def create():
    if not 'username' in session:
        return redirect(url_for('login'))
    # Expecting form data
    print(request.json['date'])
    employee = {
        "date": request.json['date'],
        "num_quit": request.json['num_quit']
    }
    values = (employee['date'], employee['num_quit'])
    newId = dataDAO.createQuitsByID(values)
    employee['id'] = newId
    return jsonify(employee)

# Route for updating employee quit data
@app.route('/employee/<int:id>', methods=['PUT'])
def update(id):
    if not 'username' in session:
        return redirect(url_for('login'))
    foundEmployee = dataDAO.findQuitsByID(id)
    if not foundEmployee:
        return jsonify({}), 404
    if not request.json:
        return jsonify({}), 400
    reqJson = request.json
    if 'date' in reqJson:
        print(reqJson['date'])
        foundEmployee['date'] = reqJson['date']
    if 'num_quit' in reqJson:
        print(reqJson['num_quit'])
        foundEmployee['num_quit'] = reqJson['num_quit']
    values = (foundEmployee['date'], foundEmployee['num_quit'], foundEmployee['id'])
    print(values)
    dataDAO.updateQuitsByID(values)
    return jsonify(foundEmployee)

# Route for deleting employee quit data
@app.route('/employee/<int:id>', methods=['DELETE'])
def delete(id):
    if not 'username' in session:
        return redirect(url_for('login'))
    dataDAO.deleteQuitsByID(id)
    return jsonify({"done": True})


# routes for generating visualizations

@app.route('/dash1')
def dash1():
    if not 'username' in session:
        return redirect(url_for('login'))
    data = dataDAO.readQuits()
    # convert data read from MySQL to dataframe
    df = pd.DataFrame(data)
    # convert date string to date
    df['date'] = pd.to_datetime(df['date'])     
    fig = px.scatter(df, x='date', y='num_quit', trendline="rolling",
                trendline_options=dict(window=5), trendline_color_override="red",
                width=1000, height=600)
    fig.update_layout(xaxis_title='Date', yaxis_title='Number of Quits')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Employee Quits by Month With Quarterly Trendline"

    # Convert date to string to format properly in plotly table (otherwise it includes timestamp)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    table = go.Figure(data=[go.Table(
                header=dict(values=['ID', 'Date', 'Number of Quits'],
                fill_color='#00008b',
                align='center', font_size=12, font_color='white'),
                cells=dict(values=[df.id, df.date, df.num_quit],
                fill_color='#e5ecf6',
                align='center', font_size=12))
            ])
    table.update_layout(width=600, height=525)
    table.update_layout(margin=dict(r=5, l=20, t=55, b=2))
    graphJSON1 = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dash1.html', graphJSON=graphJSON, header=header, graphJSON1=graphJSON1)
    

@app.route('/dash2')
def dash2():
    if not 'username' in session:
        return redirect(url_for('login'))
    data = dataDAO.readSCQuits()
    # convert data read from MySQL to dataframe
    df = pd.DataFrame(data)
    # convert date string to date
    df['date'] = pd.to_datetime(df['date'])     
    fig = px.scatter(df, x='date', y='num_quits', trendline="rolling",
                trendline_options=dict(window=5), trendline_color_override="red",
                width=1000, height=600)
    fig.update_layout(xaxis_title='Date', yaxis_title='Quits (Thousands)')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "All South Census Quits by Month With Quarterly Trendline"

    # Convert date to string to format properly in plotly table (otherwise it includes timestamp)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    table = go.Figure(data=[go.Table(
                header=dict(values=['ID', 'Date', 'Quits (Thousands)'],
                fill_color='#00008b',
                align='center', font_size=12, font_color='white'),
                cells=dict(values=[df.id, df.date, df.num_quits],
                fill_color='#e5ecf6',
                align='center', font_size=12))
            ])
    table.update_layout(width=600, height=525)
    table.update_layout(margin=dict(r=5, l=20, t=55, b=2))
    graphJSON1 = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dash2.html', graphJSON=graphJSON, header=header, graphJSON1=graphJSON1)

@app.route('/dash3')
def dash3():
    if not 'username' in session:
        return redirect(url_for('login'))
    data = dataDAO.readOpenings()
    # convert data read from MySQL to dataframe
    df = pd.DataFrame(data)
    # convert date string to date
    df['date'] = pd.to_datetime(df['date'])     
    fig = px.scatter(df, x='date', y='num_openings', trendline="rolling",
                trendline_options=dict(window=5), trendline_color_override="red",
                width=1000, height=600)
    fig.update_layout(xaxis_title='Date', yaxis_title='Job Openings (Thousands)')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "All South Census Job Openings by Month With Quarterly Trendline"

    # Convert date to string to format properly in plotly table (otherwise it includes timestamp)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    table = go.Figure(data=[go.Table(
                header=dict(values=['ID', 'Date', 'Openings (Thousands)'],
                fill_color='#00008b',
                align='center', font_size=12, font_color='white'),
                cells=dict(values=[df.id, df.date, df.num_openings],
                fill_color='#e5ecf6',
                align='center', font_size=12))
            ])
    table.update_layout(width=600, height=525)
    table.update_layout(margin=dict(r=5, l=20, t=55, b=2))
    graphJSON1 = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dash3.html', graphJSON=graphJSON, header=header, graphJSON1=graphJSON1)

@app.route('/dash4')
def dash4():
    if not 'username' in session:
        return redirect(url_for('login'))
    data = dataDAO.readUnemployment()
    # convert data read from MySQL to dataframe
    df = pd.DataFrame(data)
    # convert date string to date
    df['date'] = pd.to_datetime(df['date'])     
    fig = px.scatter(df, x='date', y='unemploymentRate', trendline="rolling",
                trendline_options=dict(window=5), trendline_color_override="red",
                width=1000, height=600)
    fig.update_layout(xaxis_title='Date', yaxis_title='Unemployment Rate %')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "South Carolina Unemployment Rate by Month With Quarterly Trendline"

    # Convert date to string to format properly in plotly table (otherwise it includes timestamp)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    table = go.Figure(data=[go.Table(
                header=dict(values=['ID', 'Date', 'Unemployment Rate %'],
                fill_color='#00008b',
                align='center', font_size=12, font_color='white'),
                cells=dict(values=[df.id, df.date, df.unemploymentRate],
                fill_color='#e5ecf6',
                align='center', font_size=12))
            ])
    table.update_layout(width=600, height=525)
    table.update_layout(margin=dict(r=5, l=20, t=55, b=2))
    graphJSON1 = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dash4.html', graphJSON=graphJSON, header=header, graphJSON1=graphJSON1)


if __name__ == '__main__' :
    app.run(debug= True)


