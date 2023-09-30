import re
from .interpreter import Interpreter

shell_prompt = """
# Run shell
* format is : ```shell\\nthe_command\\n```
* the command will be executed
"""

class ShellInterpreter(Interpreter):
    def __init__(self, workspace='./') -> None:
        self.workspace = workspace

    def prompt(self, messages) -> str:
        return shell_prompt

    @property
    def match_template(self):
        return '```shell\n(.*?)\n```'

    def parse(self, string):
        pattern = re.compile(self.match_template, re.DOTALL)
        match = pattern.search(string)
        assert match is not None
        output = self._run_bash(match.group(1))
        return output.strip(), False

    def _run_bash(self, content):
        sys_out = ''
        import subprocess
        if 'python ' in content:
            content = content.replace('python ', 'python3 ')
        try:
            p = subprocess.Popen(content, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            pass
        finally:
            sys_out, err = p.communicate()
            sys_out = sys_out.decode('utf-8')
        return sys_out