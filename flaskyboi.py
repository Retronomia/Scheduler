#testing out flask
#no hate name plz is beautiful

from flask import Flask, request,render_template
import os

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')
app = Flask(__name__, template_folder=template_path)

@app.route('/')
def hello_world():
    return render_template('index.html')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)