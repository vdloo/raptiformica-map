"use strict";

var nodes = [];
var edges = [];
var canvas = null;
var ctx = null;
var mapOffset = {x: 50, y: 50};
var zoom = 1.0;

function changeHash(hash) {
    window.location.replace(('' + window.location).split('#')[0] + '#' + hash);
}

function updateCanvasSize() {
    $(canvas).attr({height: $(canvas).height(), width: $(canvas).width()});
    ctx.translate(mapOffset.x, mapOffset.y);
}

function drawCircle(ctx, x, y, radius, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI*2, true);
    ctx.fill();
}

function drawLine(ctx, x1, y1, x2, y2, color) {
    ctx.strokeStyle = color;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.closePath();
    ctx.stroke();
}

function drawText(ctx, x, y, text, color, font) {
    ctx.fillStyle = color;
    ctx.font = font;
    ctx.textAlign = 'center';
    ctx.fillText(text, x, y);
}

function drawNetwork() {
    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.restore();


    // Draw edges
    for (var i = 0; i < edges.length; ++i) {
        var edge = edges[i];
        var highlight = edge.sourceNode.hover || edge.targetNode.hover;
        var color = highlight ? 'rgba(0, 0, 0, 0.5)' : 'rgba(0, 0, 0, 0.15)';

        drawLine(ctx,
            edge.sourceNode.x, edge.sourceNode.y,
            edge.targetNode.x, edge.targetNode.y,
            color);
    }

    // Draw nodes
    for (var i = 0; i < nodes.length; ++i) {
        var node = nodes[i];

        drawCircle(ctx, node.x, node.y, node.radius, node.color);
    }

    // Draw labels
    for (var i = 0; i < nodes.length; ++i) {
        var node = nodes[i];

        if (node.radius > 4 || node.selected || node.hover) {
            var fontSize = 4 + node.radius * 0.4;

            drawText(ctx, node.x, node.y - node.radius - 1,
                node.label, node.textColor, fontSize + 'pt "ubuntu mono"');
        }
    }
}

function moveNodesIntoView() {
    var smallest_x = 0;
    var smallest_y = 0;

    for (var i = 0; i < nodes.length; ++i) {
        var node = nodes[i];
        if (node.x < smallest_x) {
            smallest_x = node.x;
        }
        if (node.y < smallest_y) {
            smallest_y = node.y;
        }
    }
    for (var i = 0; i < nodes.length; ++i) {
        var node = nodes[i];
        node.x -= smallest_x;
        node.y -= smallest_y;
    }
}

function drawZoom(mx, my, ratio) {
    zoom *= ratio;


    for (var i = 0; i < nodes.length; ++i) {
        var node = nodes[i];
        node.x = (node.x - mx) * ratio + mx;
        node.y = (node.y - my) * ratio + my;
        node.radius = (node.size) * zoom;
    }


    drawNetwork();
}

function getNodeAt(x, y) {
    x -= mapOffset.x;
    y -= mapOffset.y;
    for (var i = nodes.length - 1; i >= 0; --i) {
        var node = nodes[i];
        var distPow2 = (node.x - x) * (node.x - x) + (node.y - y) * (node.y - y);

        if (distPow2 <= node.radius * node.radius) {
            return node;
        }
    }
    return null;
}

function searchNode(id) {
    for (var i = 0; i < nodes.length; ++i) {
        if (nodes[i].id == id)
            return nodes[i];
    }
    return null;
}

function clearNodes() {
    changeHash('');
    $('#node-info').html('');

    for (var i = 0; i < nodes.length; ++i) {
        var node = nodes[i];
        node.depth = 0xFFFF;
        node.color = node.originalColor;
        node.textColor = node.color;
        node.selected = false;
    }
}

function selectNode(node, redraw, set_hash) {
    clearNodes();

    set_hash = typeof set_hash !== 'undefined' ? set_hash : true;
    if (set_hash) {
        changeHash(node.id);
    }

    node.selected = true;
    showNodeInfo(node);

    markPeers(node, 0);
    if (redraw)
        drawNetwork();
}

function markPeers(node, depth) {
    node.depth = depth;

    var colors = ['#000000', '#096EE8', '#09E8B8', '#36E809', '#ADE809', '#E8B809', '#E87509', '#E83A09', '#E86946', '#E8AC9B', '#E8C9C1'];
    var txtCol = ['#000000', '#032247', '#034537', '#0E3D02', '#354703', '#403203', '#3D1F02', '#3B0E02', '#3B0E02', '#3B0E02', '#3B0E02'];
    node.color = (depth >= colors.length) ? '#FFFFFF' : colors[depth];
    node.textColor = (depth >= txtCol.length) ? '#FFFFFF' : txtCol[depth];

    for (var i = 0; i < node.peers.length; ++i) {
        var n = node.peers[i];
        if (n.depth > depth + 1)
            markPeers(n, depth + 1);
    }
}

function showNodeInfo(node) {
    var ip_peers = [];
    var dns_peers = [];

    for (var i = 0; i < node.peers.length; ++i) {
        var n = node.peers[i];
        if (/^[0-9A-F]{4}$/i.test(n.label))
            ip_peers.push(n);
        else
            dns_peers.push(n);
    }

    var label_compare = function(a, b) {
        return a.label.localeCompare(b.label);
    }

    dns_peers.sort(label_compare);
    ip_peers.sort(label_compare);

    var peers = dns_peers.concat(ip_peers);

    var html =
        '<h2>' + node.label + '</h2>' +
        '<span class="tt">' + node.id + '</span><br>' +
        '<br>' +
        '<strong>Version:</strong> ' + node.version + '<br>' +
        '<strong>Peers:</strong> ' + node.peers.length + '<br>' +
        '<strong>Centrality:</strong> ' + node.centrality + '<br>' +
        '<table>' +
        peers.map(function (n) {
            return '<tr>' +
                '<td><a href="#' + n.id + '" class="tt">' + n.label + '</a></td>' +
                '<td>' + n.peers.length + '</td></tr>';
        }).join('') +
        '</table>';

    $('#node-info').html(html);
}

function mousePos(e) {
    var rect = canvas.getBoundingClientRect();
    return {x: e.clientX - rect.left, y: e.clientY - rect.top};
}



$(document).ready(function() {
    canvas = document.getElementById('map');
    ctx = canvas.getContext('2d');
    updateCanvasSize();


    jQuery.getJSON('/static/graph.json', function(data) {
        nodes = data.nodes;
        edges = data.edges;

        moveNodesIntoView();

        // Calculate node radiuses
        for (var i = 0; i < nodes.length; ++i) {
            var node = nodes[i];
            node.x = node.x * 1.2;
            node.y = node.y * 1.2;
            node.radius = node.size;
            node.hover = false;
            node.selected = false;
            node.edges = [];
            node.peers = [];
            node.depth = 0xFFFF;
            node.originalColor = node.color;
            node.textColor = node.color;
        }

        var newEdges = []
        // Find node references for edges
        for (var i = 0; i < edges.length; ++i) {
            var edge = edges[i];

            for (var n = 0; n < nodes.length; ++n) {
                if (nodes[n].id == edge.sourceID) {
                    edge.sourceNode = nodes[n];
                }
                else if (nodes[n].id == edge.targetID)
                    edge.targetNode = nodes[n];
            }

            if (!edge.sourceNode || !edge.targetNode)
               continue;

            edge.sourceNode.edges.push(edge);
            edge.targetNode.edges.push(edge);
            edge.sourceNode.peers.push(edge.targetNode);
            edge.targetNode.peers.push(edge.sourceNode);

            newEdges.push(edge);
        }
        edges = newEdges;

        // Set update time
        var delta = Math.round(new Date().getTime() / 1000) - data.created;
        var min = Math.floor(delta / 60);
        var sec = delta % 60;
        $('#update-time').text(min + ' min, ' + sec + ' s ago');

        // Set stats
        $('#number-of-nodes').text(nodes.length);
        $('#number-of-connections').text(edges.length);


        var selected = false;
        if (window.location.hash) {
            var id = window.location.hash.substring(1);
            var node = searchNode(id);
            if (node) {
                selectNode(node, false);
                selected = true;
            }
        }

        if (!selected) {
            var nodes_marked_as_self = nodes.filter(function (node) {
                return node.is_self;
            });
            if (nodes_marked_as_self.length > 0) {
                node = nodes_marked_as_self[0];
                selectNode(node, false, false);
                selected = true;
            }
        }

        drawZoom(0, 0, 3);

        $(window).resize(function() {
            updateCanvasSize();
            drawNetwork();
        });


        // Initialize search
        var searchArray = [];
        for (var i = 0; i < nodes.length; ++i) {
            var node = nodes[i];

            searchArray.push({
                value: node.label,
                data: node
            });

            searchArray.push({
                value: node.id,
                data: node
            });
        }

        $('#search-box').autocomplete({
            lookup: searchArray,
            autoSelectFirst: true,
            lookupLimit: 7,
            onSelect: function(suggestion) {
                selectNode(suggestion.data, true);
            }
        });

        $('#search-box').keypress(function(e) {
            if (e.which == 13) {
                selectNode(searchNode($('#search-box').val()), true);
            }
        });

        $(document).on('click', '#node-info a', function(e) {
            var id = e.target.hash.substring(1);
            selectNode(searchNode(id), true);
        });


    });



    var mouseDownPos = null;
    var mouseLastPos = null;
    var mouseDownNode = null;
    var mouseHoverNode = null;


    $(canvas).mousemove(function(e) {
        var mouse = mousePos(e);

        // Dragging
        if (mouseDownPos != null) {
            $('body').css('cursor', 'move');
            var dx = mouse.x - mouseLastPos.x;
            var dy = mouse.y - mouseLastPos.y;
            mapOffset.x += dx;
            mapOffset.y += dy;
            ctx.translate(dx, dy);
            mouseLastPos = {x: mouse.x, y: mouse.y};
            drawNetwork();
        }
        // Hovering
        else {
            var node = getNodeAt(mouse.x, mouse.y);

            if (node == mouseHoverNode)
                return;

            if (node == null) {
                nodeMouseOut(mouseHoverNode);
            }
            else {
                if (mouseHoverNode != null)
                    nodeMouseOut(mouseHoverNode);

                nodeMouseIn(node);
            }
            mouseHoverNode = node;

            drawNetwork();
        }
    });


    $(canvas).mousedown(function(e) {
        var mouse = mousePos(e);
        mouseLastPos = mouseDownPos = {x: mouse.x, y: mouse.y};
        mouseDownNode = getNodeAt(mouse.x, mouse.y);
        return false;
    });

    $(canvas).mouseup(function(e) {
        var mouse = mousePos(e);
        var mouseMoved =
            Math.abs(mouse.x - mouseDownPos.x) +
            Math.abs(mouse.y - mouseDownPos.y) > 3

        if (!mouseMoved) {
            if (mouseDownNode)
                selectNode(mouseDownNode, true);
            else {
                clearNodes();
                drawNetwork();
            }
        }
        else {
            $('body').css('cursor', 'auto');
        }

        mouseDownPos = null;
        mouseDownNode = null;
        return false;
    });

    function handleScroll(e) {
        var mouse = mousePos(e);
        var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));

        var ratio = (delta < 0) ? (3 / 4) :  1 + (1 / 3);
        var mx = mouse.x - mapOffset.x;
        var my = mouse.y - mapOffset.y;
        drawZoom(mx, my, ratio);

    }
    canvas.addEventListener("mousewheel", handleScroll, false);
    canvas.addEventListener("DOMMouseScroll", handleScroll, false);

});

function nodeMouseIn(node) {
    node.hover = true;
    $('body').css('cursor', 'pointer');
}

function nodeMouseOut(node) {
    node.hover = false;
    $('body').css('cursor', 'auto');
}
