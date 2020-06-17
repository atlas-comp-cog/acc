<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Languages')}</%block>


<%block name="head">
    <script src="${req.static_url('acc:static/tree.jquery.js')}"></script>
    <link rel="stylesheet" href="${req.static_url('acc:static/jqtree.css')}"/>
</%block>

<h2>${_('Languages')}</h2>

        <ul class="nav nav-pills">
            <li class="">
                <a href="#tree-container">
                    <img src="${req.static_url('acc:static/Tree_Icon.png')}"
                         width="35">
                    Tree
                </a>
            </li>
            <li class="">
                <a href="#map-container">
                    <img src="${req.static_url('acc:static/Map_Icon.png')}"
                         width="35">
                    Map
                </a>
            </li>
            <li class="">
                <a href="#table-container">
                    <img src="${req.static_url('acc:static/Table_Icon.png')}"
                         width="35">
                    Table
                </a>
            </li>
        </ul>


<div class="well" id="tree-container">
    <div id="species-tree"></div>
</div>

${(map_ or request.map).render()}

<div id="table-container">
    ${ctx.render()}
</div>


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
