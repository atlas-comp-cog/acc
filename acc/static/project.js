CLLD.MapIcons.custom = function (feature, size, url) {
    size = 30;
    return L.icon({
        iconUrl: url == undefined ? feature.properties.icon : url,
        iconSize: [size, size],
        iconAnchor: [Math.floor(size / 2), Math.floor(size / 2)],
        popupAnchor: [0, 0],
        className: feature.properties['class'] == undefined ? 'clld-map-icon' : feature.properties['class']
    });
};

CLLD.mapResizeIcons = function(eid, size) {};

ACC = {};

ACC.Tree = (function(){
    var map_marker = function(node){
        return '<img src="'+node.map_marker+'" height="20" width="20">'
    };

    var marker_toggle = function(node){
        var html = '<label class="checkbox inline" style="padding-top: 0;" title="click to toggle markers">';
        html += '<input style="display: none;" type="checkbox" onclick="GLOTTOLOG3.filterMarkers(this);" ';
        html += 'class="checkbox inline" checked="checked" value="'+node.pk+'">';
        html += map_marker(node);
        html += '</label>';
        return html
    };

    return {
        init: function(eid, data, nid) {
            var e = $('#'+eid);
            e.tree({autoOpen: true, data: data, onCreateLi: ACC.Tree.node});
            if (nid){
                GLOTTOLOG3.Tree.open(eid, nid);
            }
            e.unbind('contextmenu');
        },
        node: function(node, li) {
            var title = li.find('.jqtree-title');
            //title.addClass('level-'+node.level);
            title.html(ACC.speciesLink(node));
            /*if (node.map_marker){
                if (node.child){
                    title.after(marker_toggle(node));
                } else {
                    title.after(map_marker(node));
                }
            }*/
        },
        close: function(eid) {
            var $tree = $('#' + eid);
            $tree.tree('getTree').iterate(
                function (node, level) {
                    $tree.tree('closeNode', node);
                    return true;
                }
            );
            return;
        },
        open: function(eid, nodes, scroll) {
            var el, node, top,
                $tree = $('#'+eid);

            if (!nodes) {
                $tree.tree('getTree').iterate(
                    function (node, level) {
                        if (node.level == 'dialect') {
                            return true;
                        }
                        if (!node.hasChildren()) {
                            $tree.tree('selectNode', node);
                            return false;
                        }
                        return true;
                    }
                );
                $tree.tree('selectNode', null);
                return;
            }
            nodes = nodes.split(',');
            for (var i = 0; i < nodes.length; i++) {
                node = $tree.tree('getNodeById', nodes[i]);
                el = $(node.element);
                if (top) {
                    top = Math.min(el.offset().top, top);
                } else {
                    top = el.offset().top;
                }
                el.find('span.jqtree-title').first().addClass('selected');
                $tree.tree('openNode', node);
                while (node.parent) {
                    $tree.tree('openNode', node.parent);
                    node = node.parent;
                    $(node.element).find('span.jqtree-title').first().addClass('lineage');
                }
            }
            if (top && scroll) {
                $('html, body').animate({scrollTop: top}, 500);
            }
        }
    }
})();

ACC.speciesLink = function(spec){
    spec = spec === undefined ? {} : spec;
    if (spec.id === undefined) {
        return '<span class="clf">' + spec.name + '</span>';
    }
    var cls = 'species',
        title = spec.name,
        href = CLLD.route_url('language', {'id': spec.id});
    return '<table class="species-in-tree"><tr>' +
        '<td class="bubble"><img width="' + spec.bubble_size + '" src="' + spec.bubble + '"/></td>' +
        '<td class="name"><a href="'+href+'" class="'+cls+'" title="'+title+'">'+spec.name+'</a></td>' +
        '<td><a href="'+spec.gbif_url+'"><img src="' + spec.gbif_logo + '">'+spec.gbif_name+'</a></td>' +
        '</tr></table>';
};
