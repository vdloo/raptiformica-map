raptiformica-map
================

High-available web service that visualizes a raptiformica cluster

&nbsp;  

<p align="center">
  <img src="https://raw.githubusercontent.com/vdloo/raptiformica-map/master/docs/assets/screenshot.png" alt="screenshot of network graph"/>
</p>



## Requirements

Make sure you have the system requirements
```
apt-get install python3-dev graphviz libgraphviz-dev pkg-config
```

And install the pip requirements in a virtualenv
```
mkvirtualenv -a $(pwd) -p /usr/bin/python3 raptiformica-map
pip install -r requirements/base.txt
```

if you get a `undefined symbol: Agundirected` error, run this:
```
# see https://github.com/pygraphviz/pygraphviz/issues/71
pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/" 
```


## Development

Running the tests
```
pip install -r requirements/development.txt
./runtests.sh
```


### Acknowledgements

This repository is an adaptation of [fc00.org](https://github.com/zielmicha/fc00.org)
