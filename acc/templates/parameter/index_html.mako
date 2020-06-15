<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameters')}</%block>

<h2>${title()}</h2>

<table class="table table-nonfluid">
    <thead>
    <tr>
        <th>Cognitive ability</th>
        <th>Area</th>
        <th>Domain</th>
        <th># experiments</th>
        <th># species</th>
    </tr>
    </thead>
    <tbody>
        % for param, nspecies, nex in counts:
        <tr>
            <td>${h.link(req, param)}</td>
            <td>${param.area}</td>
            <td>${param.domain_name}</td>
            <td style="text-align: right">${nex}</td>
            <td style="text-align: right">${nspecies}</td>
        </tr>
        % endfor
    </tbody>
</table>
