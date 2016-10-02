from flask import Flask, render_template, request
from raptiformica_map.graph_data import insert_graph_data

app = Flask(__name__)
app.config.from_pyfile('web_config.cfg')


def get_ip():
    return request.headers.get('x-real-ip')


@app.context_processor
def add_ip():
    return {
        'ip': get_ip()
    }


@app.route('/')
@app.route('/network')
def page_network():
    return render_template('network.html', page='network')


@app.route('/send_graph', methods=['POST'])
def page_send_graph():
    print("Receiving graph from {}".format(request.remote_addr))

    version = int(request.form.get('version', '1'))
    ret = insert_graph_data(
        ip=get_ip(),
        config=app.config,
        data=request.form['data'],
        version=version
    )
    return 'Error: {}'.format(ret) if ret else 'OK'

if __name__ == '__main__':
    app.run(host='[::1]', port=3000)
