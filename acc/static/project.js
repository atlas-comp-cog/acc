ACC = {};

ACC.close_tooltip = function () {
    d3.select('div.tooltip')
        .transition()
        .duration(500)
        .style("opacity", 0);
}

ACC.Tree = (function () {
    let node_id = function (node) {
        for (key in node) {
            if (node.hasOwnProperty(key) && key.indexOf('__id__') == 0) {
                return key.split('__id__')[1];
            }
        }
    };

    let bubble_size = function (data, node_data) {
        var nid = node_id(data);
        if (nid && node_data.hasOwnProperty(node_id(data))) {
            return node_data[node_id(data)]['bubble_size'] / 3.0;
        }
        return 10;
    };

    spacing = function (nleafs) {
        if (nleafs < 10) {
            return 60;
        }
        if (nleafs < 20) {
            return 40;
        }
        return 20;
    }

    return {
        init: function (eid, node_data, edgecolors, newick, count_leafs) {
            var svg = d3.select("#" + eid),
                tree = d3.layout.phylotree()
                    .svg(svg).size(450, '75%')
                    .spacing_x(spacing(count_leafs), true)
                    .spacing_y(spacing(count_leafs), true)
                    .radial(true),
                div = d3.select("body").append("div")
                    .attr("class", "tooltip")
                    .style("opacity", 0);

            tree.options({'draw-size-bubbles': true, 'zoom': true})
                .node_span(function (data) {
                    return bubble_size(data, node_data)
                });

            tree(d3.layout.newick_parser(newick));
            tree.style_nodes(function (element, data) {
                var j, path, paths;
                if (node_data.hasOwnProperty(data.name)) {
                    element.selectAll("circle").select(function () {
                        paths = node_data[data.name]['paths'];
                        if (paths.length === 0) {
                            d3.select(this.parentNode).insert('circle')
                                .attr('cx', 6)
                                .attr('cy', 6)
                                .attr('r', 5)
                                .attr('style', 'stroke:#000; fill:#000;')
                                .attr('transform', 'translate(-6 -6)')
                                .on("click", function () {
                                    tree.handle_node_click(data);
                                });
                        } else {
                            for (j = 0; j < paths.length; j++) {
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
                        div.html(node_data[data.name].tooltip)
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
                        div.html(
                            '<button type="button" class="close" onclick="ACC.close_tooltip()">&times;</button>' +
                            '<strong><a href="' + CLLD.route_url('language', {'id': d.id}) + '">' +
                            d.name + '</a></strong><br/>' +
                            '<em>' + d.gbif_name + '</em><br/>' +
                            d.experiments + ' experiments')
                            .style("left", (d3.event.pageX) + "px")
                            .style("top", (d3.event.pageY - 28) + "px");
                    });
                }
            })
                .style_edges(
                    function (dom_element, edge_object) {
                        var i, taxa = edge_object.source.name.split('_');
                        for (i = 0; i < taxa.length; i++) {
                            if (edgecolors.hasOwnProperty(taxa[i])) {
                                dom_element.style("stroke", edgecolors[taxa[i]]);
                                return;
                            }
                        }
                    }
                );

            tree.layout();

            $("#layout").on("click", function (e) {
                tree.radial($(this).prop("checked")).placenodes().update();
            });
        },
    }
})();
