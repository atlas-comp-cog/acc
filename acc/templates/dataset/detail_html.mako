<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
    <img class="img-polaroid" src="${req.static_url('acc:static/acc.png')}"/>
    </div>
</%def>

<h2>Welcome to the Atlas of Comparative Cognition</h2>

<p class="lead">
    The ACC is a major collaborative project that is designed to illustrate what we know about animal minds, and also 
    what we do not yet know.
    Here you can find, for the topics within animal cognition that have so far been compiled by our team, lists of the 
    experiments conducted to date, along with graphic representations of which species, for any given ability, have 
    already been studied. For example, if you click on the 'cognitive ability' tab, you will be brought to a list of 
    cognitive abilities (loosely defined) that have so far been reviewed. If you select one of these (for example 'joint
    attention', reviewed by Kirsty Graham), you will see a both a list of the experiments conducted so far on this topic
    along with a representation on a map of species of which species have so far been studied for this ability.  
    
</p>
<p>
    The site is based on data collected by an international
    <a href="${req.route_url('contributors')}">team of contributors</a>,
    and anyone can join this team if they
    are willing to put time into carrying out a systematic review of literature on a relevant topic in animal congition.
    The principles according to which the currently available data on any topic is identified follows the notion of the
    'systematic review'. This is a way to conduct what is traditionally called a literature review, but one that aims to 
    ensure that the literature identified is not arbitrary or biased. The
    <a href="${req.route_url('about', _anchor='people')}">ACC team</a>
    have created 'procedure' documents
    designed to show you how to conduct this kind of review, which are available at
    <a href="${req.route_url('about', _anchor='documents')}">About &gt; Documents</a> on this site.
    
    If you would like to conduct a systematic review or a meta-analysis, please
    <a href="${req.route_url('contact')}">contact the editors</a>
    with a topic and species you would like to work on.
</p>
