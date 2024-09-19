from saleae.range_measurements import DigitalMeasurer
from saleae.data import SaleaeTimeDelta

HIGH_HOLD_SUM = "highholdsum"
HIGH_HOLD_MEAN = "highholdmean"
HIGH_HOLD_MAX = "highholdmax"
HIGH_HOLD_MIN = "highholdmin"

class HighHoldTimeMeasurement(DigitalMeasurer):
	# Add supported_measurements here. This includes the metric
	supported_measurements = [HIGH_HOLD_SUM, HIGH_HOLD_MEAN, HIGH_HOLD_MAX, HIGH_HOLD_MIN]
	# strings that were defined in the extension.json file.

	def __init__(self, requested_measurements):
		super().__init__(requested_measurements)
		# Initialize your variables here
		self.time_max = None
		self.time_min = None
		self.last_time = None
		self.state = None
		self.is_begin = True
		self.Begin_time = None
		self.Final_time = None
		self.time_sum = None
		self.time_num = 0

	def process_data(self, data):
		for t, bitstate in data:
			# Process data here
			# First Time
			if self.is_begin is True:
				self.is_begin = False
				if bitstate is True:
					self.state = True
					self.last_time = t
				else:
					self.state = False
					# time_sum += t - self.Begin_time
			# Other Time
			else:
				if bitstate is True:
					self.last_time = t
				else:
					del_time = t - self.last_time
					if self.time_max is None:
						self.time_max = del_time
						self.time_min = del_time
						self.time_sum = del_time
						self.time_num = 1
					else:
						self.time_sum += del_time
						self.time_num += 1
						if self.time_max < del_time:
							self.time_max = del_time
						if self.time_min > del_time:
							self.time_min = del_time

	def measure(self):
		values = {}
		if self.time_sum is None:
			values[HIGH_HOLD_SUM] = 0.0
			values[HIGH_HOLD_MEAN] = 0.0
		else:
			values[HIGH_HOLD_SUM] = self.time_sum
			if self.time_num == 0:
				values[HIGH_HOLD_MEAN] = 0.0
			else:	
				values[HIGH_HOLD_MEAN] = float(self.time_sum)/self.time_num
		if self.time_max is None:
			values[HIGH_HOLD_MAX] = 0.0
		else:
			values[HIGH_HOLD_MAX] = self.time_max
		if self.time_min is None:
			values[HIGH_HOLD_MIN] = 0.0
		else:
			values[HIGH_HOLD_MIN] = self.time_min
		# Assign the final metric results here to the values object
		return values

	