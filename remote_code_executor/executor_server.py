from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
import urllib.parse
import subprocess

# in this folder
ALLOWED_COMMAND_FILE = 'commands.txt'

# allowable commands (initialized on startup)
COMMANDS = {}

class ExecuteHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def error(self, message='Error', status=400):
        msg_bytes = message.encode('utf-8')
        self.send_response(status)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", len(msg_bytes))
        self.end_headers()
        self.wfile.write(msg_bytes)


    def run_command(self, command_name) -> str | None:
        try:
            cmd = COMMANDS[command_name]
            return subprocess.check_output(cmd, shell=True)
        except KeyError:
            self.error(f'Command `{command_name}` not available.')
            return None
        except subprocess.CalledProcessError:
            # self.error(f'Unable to execute command `{command_name}`:\n{e}')
            self.error(f'Command `{command_name}` returned non-zero exit status.')
            return None

    def do_GET(self):
        if self.path[0:9] != '/command/':
            self.error('Request must have proper format /command/YOUR COMMAND')
            return

        cmd_escaped = self.path[9:]
        cmd = urllib.parse.unquote(cmd_escaped)

        cmd_output = self.run_command(cmd)

        if cmd_output is not None:
            resp = cmd_output

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(resp))
            self.end_headers()
            self.wfile.write(resp)


def run(server_class=HTTPServer, handler_class=ExecuteHandler):
    # populate the allowable commands (grab them directly from file)
    # each line can have a comment (anything after a "#" is ignored)
    # each line begins with a command name (up to ':' character)
    # command names must be unique
    with open(ALLOWED_COMMAND_FILE) as fin:
        print('populating commands from ', ALLOWED_COMMAND_FILE)
        for line in fin:
            # strip any comments
            hash_index = line.find('#')
            if hash_index >= 0:
                line = line[:hash_index]

            # skip empty lines / comment lines
            if len(line) == 0:
                continue

            # get the command name
            colon_index = line.find(':')
            cmd_name = line[:colon_index]
            if any([not ch.isalpha() and ch != '_' for ch in cmd_name]):
                print('ignoring invalid command name', cmd_name)
                continue

            if len(cmd_name) == 0:
                continue

            if cmd_name in COMMANDS:
                print('ignoring duplicate command name', cmd_name)
                continue

            # account for :<space>
            cmd = line[colon_index + 2:].strip()
            COMMANDS[cmd_name] = cmd


    print('Summary of available commands:')
    for cmd_name, cmd in COMMANDS.items():
        print(cmd_name)



    server_address = ('127.0.0.1', 8234)
    print('Starting HTTP server', server_address)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()