import sys
modPath='/home/shan/projects/davids/research/programs/PersonalReadbilityCalculation/'
sys.path.append(modPath)

from flask import Flask, jsonify, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)


import nltk
import re

from grammarStructure import GrammarStructure
from utilities import utilities
from shanDavReadability import Readability


app = Flask(__name__)


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'sentient_nodejsu'
app.config['MYSQL_DATABASE_PASSWORD'] = 'node@123'
app.config['MYSQL_DATABASE_DB'] = 'practice_BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

def getReadability(username, text):
	userModelPath=modPath+'profiles/'+username
	testText = ['text1.txt', 'A grand plan.txt']
	if text == '':
		text = open(modPath+'texts/'+testText[0], 'r').read().lower()
	regexAlpha = re.compile('[^a-z.!]')
	text = regexAlpha.sub(' ', text) 
	text = re.sub(' +',' ', text)

	gs = GrammarStructure(''); 
	learnerVocab, learnerGrammar=gs.loadUserProfileFromFile(userModelPath + '/vocabulary.json', userModelPath +'/grammar.json');
	sentences = gs.getSentencesFromText(text.lower())
	posList, wordList = gs.getPOS_List(sentences) 
    
	rd = Readability(text, utilities())
	utils = utilities()
	familiarWords = utils.common_elements( rd.analyzedVars['words'], learnerVocab)
	difficultWords = utils.unfamiliarWords( rd.analyzedVars['words'], learnerVocab)
	familiarGrammar, unfamiliarGrammar = utils.common_grammar( posList, learnerGrammar)
	rd.setLearnerVocabulary(learnerVocab, familiarWords, difficultWords)
	rd.setLearnerGrammar(learnerGrammar, familiarGrammar, unfamiliarGrammar)

	return 'Dav-Shan Text Difficulty Score (familiar vocabulary): '+ str(rd.shanDav(True)), learnerVocab, learnerGrammar

#def createUser():
#	cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
#	if len(data) is 0:
#	    conn.commit()
#	    return json.dumps({'message':'User created successfully !'})
#	else:
#	    return json.dumps({'error':str(data[0])})


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route("/")
def landing():
	return render_template('index.html')
    #return "Hello World!"

@app.route("/main")
def main():
	return render_template('main.html')


@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _email and _password:
        #return json.dumps({'html':'<span>All fields good !!</span>'})
        _hashed_password = generate_password_hash(_password)
        #print (_hashed_password)
        cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
        data = cursor.fetchall()
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})



@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/readability/api1.0/get_readability', methods=['GET'])
def get_readability():
    return jsonify({'score': getReadability()})

@app.route('/readability/api1.0/user_readability', methods=['POST'])
def user_readability():
    print request.form['user_name']; return jsonify({'score': getReadability(request.form['user_name'], request.form['test_text'])})

@app.route('/readability/api1.0/get_users', methods=['GET'])
def get_users():
	with open(modPath+'profiles/users') as fp: users = fp.read().splitlines()
	return jsonify({'users': users})



@app.route('/user/<username>')
def show_user_profile(username):
	readability, learnerVocab, learnerGrammar = getReadability(username, ''); #print learnerGrammar
    
	return render_template('user.html', username=username, readability=readability, learnerVocab=learnerVocab, learnerGrammar=learnerGrammar)


if __name__ == '__main__':
    app.run(debug=True)