import flask
import subprocess
from flask import stream_with_context

app = flask.Flask(__name__)

from easyLDA import main

path = 'sample.txt'
topics = 3
n_gram = 3

@app.route( '/stream' )
def stream():
    path = 'sample.txt'

    main()
    
    def generator():
        
        for i in out:
            yield i




    return flask.Response( stream_with_context(generator()), mimetype= 'text/event-stream' )

@app.route('/page')
def get_page():
    return flask.send_file('page.html')

if __name__ == "__main__":
    app.run(debug=True)
