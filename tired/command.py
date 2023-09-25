import subprocess
from shlex import split
import tired.logging


_CONTEXT = "tired.command"


def listout(l: list):
	command_string = '> ' + ' '.join(l)
	tired.logging.debug(_CONTEXT, f"Executing command `{command_string}`")


def get_output_piped(commands, verbose=False):
	"""
	:param commands: commands to execute. The commands are executed in a sequential manner, i.e. piped
	:return: console output, string
	"""
	commands = [split(c) for c in commands]
	procs = []

	listout(commands[0])
	p = subprocess.Popen(commands[0], stdout=subprocess.PIPE)

	for c in commands[1:]:
		tired.logging.debug(_CONTEXT, "  ↑ piped into ↓")
		listout(c)
		p = subprocess.Popen(c, stdout=subprocess.PIPE, stdin=p.stdout)

	p.wait()
	out = p.stdout.read()

	if verbose and len(out):
		print(out.decode("unicode_escape"))

	return out, p.returncode


def get_output(cmd):
	tired.logging.debug(_CONTEXT, "Executing command " + '>  `' + cmd + '`')
	ret = subprocess.run(split(cmd), stdout=subprocess.PIPE)

	if ret.returncode != 0:
		raise Exception("Command execution error")

	return ret.stdout.decode("unicode_escape").strip()


def get_output_with_code(cmd):
	tired.logging.debug(_CONTEXT, "Executing command " + '>  `' + cmd + '`')
	ret = subprocess.run(split(cmd), stdout=subprocess.PIPE)

	return ret.stdout.decode("unicode_escape").strip(), ret.returncode


def execute(cmd):
	tired.logging.debug(_CONTEXT, "Executing command " + '>  `' + cmd + '`')
	ret = subprocess.run(split(cmd))

	if ret.returncode != 0:
		raise Exception(f"Command execution error (returncode - {ret.returncode})")
