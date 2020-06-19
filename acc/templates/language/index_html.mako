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
        % for cls, (color, url) in tree.data['colormap'].items():
            circle.${cls} {
                fill: ${color};
            }
        % endfor
            % for cls, (color, url) in tree.data['colormap2'].items():
                circle.${cls} {
                    fill: ${color};
                }
            % endfor
    </style>
</%block>

<h2>${_('Languages')}</h2>

<p>
    Taxonomical data has been added to the <em>Atlas of Comparative Cognition</em> from the
    GBIF Backbone Taxonomy.
</p>
<blockquote>
    GBIF Secretariat (2019). GBIF Backbone Taxonomy. Checklist dataset https://doi.org/10.15468/39omei
</blockquote>

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#radial" data-toggle="tab">
            <img src="${req.static_url('acc:static/Tree_Icon.png')}" width="35">
            Tree
        </a></li>
        <li><a href="#table" data-toggle="tab">
            <img src="${req.static_url('acc:static/Table_Icon.png')}" width="35">
            Table
        </a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="radial" class="tab-pane active">
            ${tree.render()}
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
