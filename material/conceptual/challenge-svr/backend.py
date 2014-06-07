
class BaseBackend(object):
	def validate(self, username, token, salt):
		return None

class TestBackend(BaseBackend):
	def validate(self, username, token, salt):
		return True

def DefaultBackend():
	return TestBackend()
