import flask
from shelljob import proc

import eventlet
eventlet.monkey_patch()

app = flask.Flask(__name__)

@app.route( '/stream' )
def stream():
    g = proc.Group()
    p = g.run( [ "bash", "-c", "for ((i=0;i<100;i=i+1)); do echo $i; sleep 1; done" ] )

    def read_process():
        while g.is_pending():   
            lines = g.readlines()
            for proc, line in lines:
                yield "data:" + line + "\n\n"

    return flask.Response( read_process(), mimetype= 'text/event-stream' )

@app.route('/page')
def get_page():
    return flask.send_file('page.html')

if __name__ == "__main__":
    app.run(debug=True)
