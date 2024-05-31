# helpers functions
from subprocess import Popen, PIPE


def run_shell_command(command, ignore_errors=False):
    """Execute external command"""

    p1 = Popen(
        command,
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
        env={"PATH": "/usr/local/bin:/usr/bin:/bin"},
        universal_newlines=True,
    )
    output, err = p1.communicate()
    if err or "error" in output.lower() or "failed" in output.lower():
        if not ignore_errors:
            print(output, err)
        return False
    if output:
        return output
    else:
        return err


def extract_ips(filename: str):
    """Extract unque IP's from log file
    expecting first word in line is IP address"""

    command = f"grep 'Googlebot\|yandex.com/bots' {filename} | cut -d ' ' -f 1 |sort | uniq"

    result = run_shell_command(command)
    return result
