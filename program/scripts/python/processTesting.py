import threading, time, subprocess
from enum import Enum

class ThreadedCommand:

	def __init__(self, cmd):
		self.command = cmd
		self.process = None
		self.terminated = False
		
		self.stdout = None
		self.stderr = None
		self.exitCode = None
	def run(self, timeout):
		def target():
			print 'Thread started'
			self.process = subprocess.Popen(self.command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			(self.stdout, self.stderr) = self.process.communicate()
			self.exitCode = self.process.returncode
			print 'Thread finished'

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			print 'Terminating process'
			self.process.terminate()
			thread.join()
osProcess = ThreadedCommand(["echo", "whatsupworld"])
osProcess.run(5)
time.sleep(6)
print osProcess.stdout