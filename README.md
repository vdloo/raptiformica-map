raptiformica-map
================

High-available web service that visualizes a raptiformica cluster


## Requirements

Make sure you have the system requirements
```
apt-get install python3-dev libmysqlclient-dev graphviz libgraphviz-dev pkg-config
```

And install the pip requirements in a virtualenv
```
mkvirtualenv -a $(pwd) -p /usr/bin/python3 raptiformica-map
pip install -r requirements/base.txt

```

# if you get a `undefined symbol: Agundirected` error, run this:
```
pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/" 
# see https://github.com/pygraphviz/pygraphviz/issues/71
```


## Development

Running the tests
```
pip install -r requirements/development.txt
./runtests.sh
```


### Acknowledgements

This repository is an adaptation of [fc00.org](https://github.com/zielmicha/fc00.org)
