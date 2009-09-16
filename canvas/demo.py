# Demonstration of the Process Canvas.
# Sample network.

from model import Process, ChanEnd, Network

delta =  Process(name='Delta',
                input_chans=[
                    ChanEnd('in.0', 'input', 'INT'),
                    ChanEnd('in.1', 'input', 'INT')
                ],
                output_chans=[
                    ChanEnd('out', 'output', 'INT')
                ]
        )

integrate = Process(name='Integrate',
                    input_chans=[
                        ChanEnd('in', 'input', 'BOOL')
                    ],
                    output_chans=[
                        ChanEnd('out', 'output', 'BOOL')
                    ]
            )

n = Network()
n.add_process(delta)
n.add_process(integrate)