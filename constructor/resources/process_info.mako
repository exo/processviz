<%inherit file="base.mako" />
<h3>Process: <code>${name}</code></h3>
<p>${desc}
<ul>
    %if input is not UNDEFINED:
    <li><strong>Inputs: </strong>
    %if input is not None:
    %for i in input:
        ${i['desc']}, 
    %endfor
    %else:
    None
    %endif
    </li>
    %endif
    %if output is not UNDEFINED:
    <li><strong>Outputs: </strong>
    %if output is not None:
    %for o in output:
        ${o['desc']}, 
    %endfor
    %else:
    None
    %endif
    </li>
    %endif
    <li><strong>Parameters:</strong> None</li>
</ul>
</p>
