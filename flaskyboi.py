#testing out flask
#no hate name plz is beautiful

from flask import Flask, request,render_template
import os
import urllib

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')
app = Flask(__name__, template_folder=template_path)
message = dict()


@app.route('/')
def hello_world():
    return render_template('index.html')



@app.route('/', methods=['post', 'get'])
def getform():
    if request.method == 'POST':
        if "form" in request.form:
            if request.form["form"] == "const":
                quarter = request.form.get('quarter')  # access the data inside 
                year = request.form.get('year')
                time = request.form.get('time')
                message['quarter'] = quarter
                message['year'] = year
                message['time'] = time
            elif request.form["form"] == "speccourse":
                department = request.form.get('department')
                cnumber = request.form.get('course-number')
                if 'courses' in message:
                    if (cnumber,department) not in message['courses']:
                        message['courses'].append((cnumber,department))
                else:
                    message['courses'] = [(cnumber,department)]
        elif 'course_rem' in request.form and 'courses' in message:
            del message['courses'][int(request.form['course_rem'])]

    return render_template('index.html', message=message)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)