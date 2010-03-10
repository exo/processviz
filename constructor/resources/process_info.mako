<%inherit file="base.mako" />
<h3>Process: <code>${name}</code></h3>
<p>${desc}</p>

%if input is not UNDEFINED and input is not None:
<h4>Inputs</h4>
<ul>
%for i in input:
    <li><tt>${i['name']}</tt> &ndash; ${i['desc']}</li>
%endfor
</ul>
%endif

%if output is not UNDEFINED and output is not None:
<h4>Outputs</h4>
<ul>
%for o in output:
    <li><tt>${o['name']}</tt> &ndash; ${o['desc']}</li>
%endfor
</ul>
%endif

%if params is not UNDEFINED and params is not None:
<h4>Parameters</h4>
<ul>
%for p in params:
    <li><tt>${p['name']}</tt> &ndash; ${p['desc']}</li>
%endfor
</ul>
%endif
