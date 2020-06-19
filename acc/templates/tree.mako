<div style="float: left; width: 20%">
    <table class="table table-condensed table-nonfluid" style="float: left;">
        <thead>
        <tr>
            <th></th>
            <th>Class</th>
        </tr>
        </thead>
        <tbody>
            % for cls, (color, url) in obj.data['colormap2'].items():
                <tr>
                    <td style="color: ${color}; font-weight: bold">━</td>
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
            % for cls, (color, url) in obj.data['colormap'].items():
                <tr>
                    <td><img style="opacity: 0.7" width="20" src="${url}"/></td>
                    <td>${cls}</td>
                </tr>
            % endfor
        </tbody>
    </table>
</div>
<svg id="tree_display" style="width: 70%">
</svg>
<script>
$(document).ready(function() {
${h.JS('ACC.Tree').init('tree_display', obj.data['node_data'], obj.data['edgecolors'], obj.data['newick'], obj.data['count_leafs'])|n};
});
</script>
