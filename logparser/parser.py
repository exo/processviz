INS, AJW, START, END, CALL, OUTPUT, INPUT = 'INS AJW START END CALL OUTPUT INPUT'.split(' ')

class LogParser (object):
    
    def __init__ (self, path):
        self.file = open(path)

    def parse_list (self, data):
        for line in data:
            print parse(line)
            
    def next (self):
        line = self.file.readline()
        if line:
            return self.parse(line)
        else:
            return None

    def parse (self, line):
        d = line.strip().split(' ')
        address, cmd = int(d[0], 16), d[1]
        if cmd == '@':
            # Instruction executed.
            filename, line_no = d[2].split(':')
            return [INS, address, filename, int(line_no)]
        elif cmd == '=>':
            # Rename process
            new_address = int(d[2], 16)
            return [AJW, address, new_address]
        elif cmd == 'start':
            # Start process
            new_address = int(d[2], 16)
            return [START, address, new_address]
        elif cmd == 'end':
            # End process
            return [END, address]
        elif cmd == 'call':
            # Call
            return [CALL, address, d[2]]
        elif cmd == 'output':
            channel = int(d[2], 16)
            return [OUTPUT, address, channel]
        elif cmd == 'input':
            channel = int(d[2], 16)
            return [INPUT, address, channel]
        else:
            raise Exception("Unknown op type '%s'" % cmd)

#parse_list(open('commstime.log'))