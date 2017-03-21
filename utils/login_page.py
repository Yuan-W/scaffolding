from flask import Flask , request , abort , redirect , Response ,url_for

app = Flask(__name__)

@app.route('/' , methods=['GET' , 'POST'])
@app.route('/login' , methods=['GET' , 'POST'])
def login():
	if request.method == 'POST':
		return redirect('http://127.0.0.1:5000/dashboard', code=307)
	else:
		return Response('''
        <form action="" method="post">
            authorization code<br><input type=text name=authorization_code value=2d580804fc6a5d598abfe0514fa6ad61d34f5010><br>
            <p>authorized<br><input type=text name=authorized value=Yes>
            <p><input type=submit value=Login>
        </form>
        ''')
 
if __name__ == '__main__':
	app.run(port=4999, debug =True)
