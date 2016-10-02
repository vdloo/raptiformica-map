from flask import Flask, render_template, request
from graphData import insert_graph_data

app = Flask(__name__)
app.config.from_pyfile('web_config.cfg')

def get_ip():
        try:
                ip = request.headers['x-real-ip']
        except KeyError:
                ip = None
        if ip == '10.18.3.20':
                ip = request.headers['x-atomshare-real-ip']
        return ip

@app.context_processor
def add_ip():
        return dict(ip=get_ip())


@app.route('/')
@app.route('/network')
def page_network():
    return render_template('network.html', page='network')

@app.route('/about')
def page_about():
    return render_template('about.html', page='about')

@app.route('/sendGraph', methods=['POST'])
def page_sendGraph():
    print "Receiving graph from %s" % (request.remote_addr)

    data = request.form['data']
    mail = request.form.get('mail', 'none')
    version = int(request.form.get('version', '1'))
    ret = insert_graph_data(ip=get_ip(), config=app.config, data=data, mail=mail, version=version)

    if ret == None:
        return 'OK'
    else:
        return 'Error: %s' % ret

if __name__ == '__main__':
    app.run(host='localhost', port=3000)
