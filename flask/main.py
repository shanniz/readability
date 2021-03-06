import json
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
from helpers import Struct, helpers
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

def getReadability(username, text, easeThreshold=5.0):
	userModelPath=modPath+'profiles/'+username
	#testText = ['text1.txt', 'A grand plan.txt']
	testText = ['level3/text1.txt', 'level2/Jane with Mom.txt', 'level1/A grand plan.txt']
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
	unfamiliarWords = utils.unfamiliarWords( rd.analyzedVars['words'], learnerVocab)
	familiarGrammar, unfamiliarGrammar = utils.common_grammar( posList, learnerGrammar)
	rd.setLearnerVocabulary(learnerVocab, familiarWords, unfamiliarWords)
	rd.setLearnerGrammar(learnerGrammar, familiarGrammar, unfamiliarGrammar)

	score = rd.shanDav(retDifficulty = True)
	level = "Easy"
	if score>easeThreshold:
		level = 'Difficult'
	readability = {
		'score': score, 
		'level': level, 
		'learnerVocab': learnerVocab, 
		'learnerGrammar': learnerGrammar, 
		'unfamiliarWords': unfamiliarWords,
		'unfamiliarGrammar': unfamiliarGrammar

	}

	return  score, learnerVocab, learnerGrammar, level

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
	return render_template('main.html')
    #return "Hello World!"

@app.route("/index")
def index():
	return render_template('index.html')

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


@app.route('/readability/api1.0/user_readability', methods=['POST'])
def user_readability():
    #print request.form['user_name']; 
    return jsonify({'score': getReadability(request.form['user_name'], request.form['test_text'], float (request.form['range_ease_threshold']) ) })

@app.route('/readability/api1.0/get_users', methods=['GET'])
def get_users():
	with open(modPath+'profiles/users') as fp: users = fp.read().splitlines()
	return jsonify({'users': users})

@app.route('/readability/api1.0/config/set', methods=['POST'])
def set_config():
	jsonObj = helpers.read_JSON('/home/shan/projects/davids/research/programs/PersonalReadbilityCalculation/flask/readabilityConfig.json')
	jsonObj['easeThreshold'] = float (request.form['range_ease_threshold'])
	helpers.save_JSON(jsonObj, '/home/shan/projects/davids/research/programs/PersonalReadbilityCalculation/flask/readabilityConfig.json')
	return "success!"

@app.route('/user/<username>')
def show_user_profile(username):
	jsonObj = helpers.read_JSON('/home/shan/projects/davids/research/programs/PersonalReadbilityCalculation/flask/readabilityConfig.json')
	conf = Struct(**jsonObj)
	#'level': level, 'learnerVocab': learnerVocab, 'learnerGrammar': learnerGrammar, 
	#'unfamiliarWords': unfamiliarWords,		'unfamiliarGrammar': unfamiliarGrammar
	readability, learnerVocab, learnerGrammar, level = getReadability(username, '', conf.easeThreshold); #print learnerGrammar
	#readability = getReadability(username, '', conf.easeThreshold);
	return render_template('userSub.html', username=username, readability=readability, learnerVocab=learnerVocab, 
		learnerGrammar=learnerGrammar
	, config=conf)


@app.route('/user/learn/')
def show_user_learn():
	#jsonObj = helpers.read_JSON('/home/shan/projects/davids/research/programs/PersonalReadbilityCalculation/flask/readabilityConfig.json')
	#conf = Struct(**jsonObj)
	#'level': level, 'learnerVocab': learnerVocab, 'learnerGrammar': learnerGrammar, 
	#'unfamiliarWords': unfamiliarWords,		'unfamiliarGrammar': unfamiliarGrammar
	#readability, learnerVocab, learnerGrammar, level = getReadability(username, '', conf.easeThreshold); #print learnerGrammar
	#readability = getReadability(username, '', conf.easeThreshold);
	return render_template('learn.html') # , username=username)

if __name__ == '__main__':
    app.run(debug=True)