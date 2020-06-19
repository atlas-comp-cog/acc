<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>

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


<h2>${_('Parameter')} ${ctx.name}</h2>

% if ctx.description:
<p>${ctx.description}</p>
% endif

        <ul class="nav nav-pills">
            <li class="">
                <a href="#tree-container">
                    <img src="${req.static_url('acc:static/Tree_Icon.png')}" width="35">
                    Species
                </a>
            </li>
            <li class="">
                <a href="${req.resource_url(ctx) if tree else ''}#table-container">
                    <img src="${req.static_url('acc:static/Table_Icon.png')}" width="35">
                    Experiments
                </a>
            </li>
        </ul>

<div id="tree-container">
    ${tree.render()|n}
</div>

<div id="table-container">
    ${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
</div>
