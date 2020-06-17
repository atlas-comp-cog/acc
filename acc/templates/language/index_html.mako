<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Languages')}</%block>

<%def name="sidebar()">
    % if map_ or request.map:
        ${(map_ or request.map).render()}
    % endif
</%def>

<%block name="head">
    <script src="${req.static_url('acc:static/tree.jquery.js')}"></script>
    <link rel="stylesheet" href="${req.static_url('acc:static/jqtree.css')}"/>
</%block>

<h2>${_('Languages')}</h2>

<div class="well">
    <div id="species-tree"></div>
</div>

${ctx.render()}


<script>
    $(document).ready(function () {
        var data = ${tree|n};
            $('#species-tree').tree({
        data: data,
                autoOpen: true,
                onCreateLi: ACC.Tree.node
    });
    });
</script>
