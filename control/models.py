from django.db import models

# Create your models here.
class ContestSettings(models.Model):
	startTime 			= models.DateTimeField()
	endTime 			= models.DateTimeField()
	paused				= models.BooleanField(default=False)

	name 				= models.TextField()
	deduction 			= models.IntegerField(default=0)

	def inSession(self, time):
		return self.startTime <= time and time <= self.endTime and not self.paused

	def __unicode__(self):
		return "%s -- Start: %s. End: %s. Paused? %s" % (self.name, self.startTime, self.endTime, self.paused)
