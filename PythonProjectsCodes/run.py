from flask import Flask, render_template, send_from_directory
app = Flask(__name__)

@app.route('/')
def start():
   return render_template('index.html')

@app.route('/templage')
def template():
   return send_from_directory('/static/template.xlsx')


#@app.route('/html/<ID>')
#def pics(ID):
#   return render_template('html/{}'.format(ID))

@app.route('/<path:values>')
def ALL(values):
   return render_template('{}'.format(values))



if __name__ == '__main__':
   app.run(debug = True,host='0.0.0.0',port=250)
