<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Languages')}</%block>


<%block name="head">
  <script src="//d3js.org/d3.v3.min.js"></script>
  <script src="//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"></script>
  <link href="${req.static_url('acc:static/phylotree.css')}" rel="stylesheet">
  <script src="${req.static_url('acc:static/phylotree.js')}"></script>
</%block>

<h2>${_('Languages')}</h2>

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#radial" data-toggle="tab">
                <img src="${req.static_url('acc:static/Map_Icon.png')}" width="35">
                Map
        </a></li>
        <li><a href="#tree" data-toggle="tab">
            <img src="${req.static_url('acc:static/Tree_Icon.png')}"
                 width="35">
            Tree
        </a></li>
        <li><a href="#table" data-toggle="tab">
            <img src="${req.static_url('acc:static/Table_Icon.png')}"
                 width="35">
            Table
        </a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="radial" class="tab-pane active">
            <svg id="tree_display">
            </svg>
        </div>
        <div id="tree" class="tab-pane">
            <div id="species-tree"></div>
        </div>
        <div id="table" class="tab-pane">
            ${ctx.render()}
        </div>
    </div>
    <script>
$(document).ready(function() {
    if (location.hash !== '') {
        $('a[href="#' + location.hash.substr(2) + '"]').tab('show');
    }
    return $('a[data-toggle="tab"]').on('shown', function(e) {
        return location.hash = 't' + $(e.target).attr('href').substr(1);
    });
});
    </script>
</div>



<script>
    $(document).ready(function () {
        var svg = d3.select("#tree_display");
        var node_data = ${node_data|n};
        var tree = d3.layout.phylotree()
                .svg(svg).size(500, '100%')
                .radial(true);
        var a = svg.append('a').attr('href', '#').attr('id', 'mouseover-text-link');
    a.append('text')
    .attr('id', 'mouseover-text')
    .attr('transform', 'translate(10, 10)').attr('fill', '#999')
    .text('selected species');

        node_id = function(node) {
            for (key in node) {
                if (node.hasOwnProperty(key) && key.indexOf('__id__') == 0) {
                    return key.split('__id__')[1];
                }
            }
        };

        bubble_size = function(data){
          var nid = node_id(data);
          if (nid && node_data.hasOwnProperty(node_id(data))) {return node_data[node_id(data)]['bubble_size'] / 3.0;};
          return 10;
        };

        tree.options({'draw-size-bubbles': true, 'zoom': true}).node_span(bubble_size);

        tree(d3.layout.newick_parser("${newick}"));
        tree.style_nodes(function(element, data) {
            if (node_data.hasOwnProperty(node_id(data))) {
                var d = node_data[node_id(data)];
                element.on('mouseover', function () {
                    d3.select('#mouseover-text-link').attr('href', CLLD.route_url('language', {'id': d.id}));
                    d3.select('#mouseover-text').attr('fill', 'black').attr('text-decoration', 'underline')
                            .text(d.gbif_name + ': ' + d.experiments + ' experiments');
                });
            }
        });

        tree.layout();

        $("#layout").on("click", function(e) {
            tree.radial($(this).prop("checked")).placenodes().update();
        });



        var data = ${tree|n};
            $('#species-tree').tree({
        data: data,
                autoOpen: true,
                onCreateLi: ACC.Tree.node
    });
    });
</script>
