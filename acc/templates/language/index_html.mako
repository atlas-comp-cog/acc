<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Languages')}</%block>


<%block name="head">
  <script src="//d3js.org/d3.v3.min.js"></script>
  <script src="//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"></script>
  <link href="${req.static_url('acc:static/phylotree.css')}" rel="stylesheet">
  <script src="${req.static_url('acc:static/phylotree.js')}"></script>
    <style>
        % for cls, (color, url) in colormap.items():
            circle.${cls} {
                fill: ${color};
            }
        % endfor
            % for cls, (color, url) in colormap2.items():
                circle.${cls} {
                    fill: ${color};
                }
            % endfor
    </style>
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
            <div style="float: left; width: 20%">
                <table class="table table-condensed table-nonfluid" style="float: left;">
                    <thead>
                    <tr>
                        <th></th>
                        <th>Class</th>
                    </tr>
                    </thead>
                    <tbody>
                    % for cls, (color, url) in colormap2.items():
                    <tr>
                        <td style="color: ${color}; font-weight: bold">─</td>
                        <td>${cls}</td>
                    </tr>
                    % endfor
                    </tbody>
                </table>
                <table class="table table-condensed table-nonfluid" style="float: left;">
                    <thead>
                    <tr>
                        <th></th>
                        <th>Family</th>
                    </tr>
                    </thead>
                    <tbody>
                        % for cls, (color, url) in colormap.items():
                            <tr>
                                <td><img width="20" src="${url}"/></td>
                                <td>${cls}</td>
                            </tr>
                        % endfor
                    </tbody>
                </table>
            </div>
            <svg id="tree_display" style="width: 60%">
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
                .svg(svg).size(450, '75%').spacing_x(20, true).spacing_y(20, true)
                .radial(true);
        var edgecolors = ${edgecolors|n};

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

        var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

        close_tooltip = function() {
            div.transition()
                    .duration(500)
                    .style("opacity", 0);
        }

        tree.options({'draw-size-bubbles': true, 'zoom': true}).node_span(bubble_size);

        tree(d3.layout.newick_parser("${newick}"));
        tree.style_nodes(function(element, data) {
            if (node_data.hasOwnProperty(data.name)) {
               //element.selectAll("circle").attr('class', data.name.replace('_', ' '));
               // can we replace the circle with a pie chart?
                element.selectAll("circle").select(function () {
                    var j, path, paths = node_data[data.name]['paths'];
                    if (paths.length == 0) {
                        d3.select(this.parentNode).insert('circle')
                        .attr('cx', 6).attr('cy', 6).attr('r', 5).attr('style', 'stroke:#000; fill:#000;')
                                .attr('transform', 'translate(-6 -6)')
                       .on("click", function () {
                                tree.handle_node_click(data);
                            });
                    } else {
                        for (j=0; j<paths.length; j++) {
                            path = d3.select(this.parentNode).insert('path');
                            for (attr in paths[j]) {
                                if (paths[j].hasOwnProperty(attr)) {
                                    path.attr(attr, paths[j][attr]);
                                }
                            }
                            path.on("click", function () {
                                tree.handle_node_click(data);
                            });
                        }
                    }
                    d3.select(this).remove();
                })
                element.on('mouseover', function () {
                    div.transition()
                            .duration(200)
                            .style("opacity", .95);
                    div	.html(node_data[data.name].tooltip)
                            .style("left", (d3.event.pageX) + "px")
                            .style("top", (d3.event.pageY - 28) + "px");
                });
                element.on('mouseout', function () {
                    div.transition()
                            .duration(500)
                            .style("opacity", 0);
                });
            }
            if (node_data.hasOwnProperty(node_id(data))) {
                var d = node_data[node_id(data)];
                element.selectAll("circle").attr('class', 'bubble ' + d.family);

                element.on('mouseover', function () {

            div.transition()
                .duration(200)
                .style("opacity", .95);
            div	.html(
                '<button type="button" class="close" onclick="close_tooltip()">&times;</button>' +
                '<strong><a href="' + CLLD.route_url('language', {'id': d.id}) + '">' + d.name + '</a></strong><br/>' +
                '<em>' + d.gbif_name + '</em><br/>' +
                d.experiments + ' experiments')
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
            });
            }
        })
        .style_edges(
           function(dom_element, edge_object) {
               var i, taxa = edge_object.source.name.split('_');
               for (i=0; i<taxa.length;i++) {
                   if (edgecolors.hasOwnProperty(taxa[i])) {
                       dom_element.style("stroke", edgecolors[taxa[i]]);
                       return;
                   }
               }
      }
        );

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
