import threading, time, subprocess


class TimeoutThread:
	def __init__(self, cmd):
		self.command = cmd
		self.process = None
		self.terminated = False
		
		self.stdout = None
		self.stderr = None
		self.exitCode = None
	def run(self, timeout):
		def target():
			self.process = subprocess.Popen(self.command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			(self.stdout, self.stderr) = self.process.communicate()
			self.exitCode = self.process.returncode

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			self.process.terminate()
			thread.join()
			self.terminated = True



osProcess = TimeoutThread(["python", "infiniteloop.py"])
osProcess.run(3)
print osProcess.terminated
if osProcess.terminated:
	print "process terminated"
else:
	print "process finished"
	print osProcess.stdout
	print osProcess.stderr
print "return code %i" % (osProcess.exitCode)
