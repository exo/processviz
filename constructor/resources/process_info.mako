<%inherit file="base.mako" />
<h3>Process: <code>${name}</code></h3>
<p>${desc}
<ul>
	%if input is not UNDEFINED:
	<li><strong>Inputs: </strong>
	%for i in input:
		${i['desc']}, 
	%endfor
	</li>
	%endif
	%if output is not UNDEFINED:
	<li><strong>Outputs: </strong>
	%for o in output:
		${o['desc']}, 
	%endfor
	</li>
	%endif
	<li><strong>Parameters:</strong> none</li>
</ul>
</p>