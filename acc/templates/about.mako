<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>

<%def name="sidebar()">
    <div class="well well-small">
        <h3>Contents</h3>
        <ul>
            <li><a href="#people">People</a></li>
            <li><a href="#documents">Documents</a></li>
        </ul>
    </div>
</%def>

<h3>About the <em>Atlas of Comparative Cognition</em></h3>

<%util:section title="People" level="4" id="people">
    <p>
        The <em>Atlas of Comparative Cognition</em> is a collaborative effort.
        Several people contributed significantly during the initial phase of the project:
    </p>
    <table class="table table-nonfluid table-striped">
        <thead><tr><th>Name</th><th>Role</th></tr></thead>
        <tbody>
        <tr>
            <td>Robert Forkel</td><td>data modeling</td>
        </tr>
        <tr>
            <td>Mélissa Berthet</td><td>vetting of the review procedure</td>
        </tr>
        <tr>
            <td>Guillaume Dezecache</td><td>vetting of the review procedure</td>
        </tr>
        <tr>
            <td>Kirsty Graham</td><td>vetting of the review procedure</td>
        </tr>
        </tbody>
    </table>
</%util:section>

<%util:section title="Documents" level="4" id="documents">
    <p>
        The following documents describe our review procedure and can serve as a starting point
        for contributions:
    </p>
    <dl>
        <dt><a href="${req.static_url('acc:static/docs/ACC_review_procedure.pdf')}">Review procedure [PDF]</a></dt>
        <dd>A description of the procedure for systematic reviews.</dd>
        <dt><a href="${req.static_url('acc:static/docs/ACC_review_template.xlsx')}">Review template [XLSX]</a></dt>
        <dd>An excel workbook providing the data structure for systematic reviews as editable
        spreadsheets.</dd>
    </dl>
</%util:section>
