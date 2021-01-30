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



@app.route('/', methods=['post', 'get'])
def getform():
    message = ''
    if request.method == 'POST':
        quarter = request.form.get('quarter')  # access the data inside 
        year = request.form.get('year')
        department = request.form.get('department')
        cnumber = request.form.get('course-number')
        time = request.form.get('time')
        message = f'Data Retrieved: {quarter},{year},{department},{cnumber},{time}'
    return render_template('index.html', message=message)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)