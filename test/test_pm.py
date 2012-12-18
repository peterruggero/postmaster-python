import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import postmaster


class PostmasterTestCase(unittest.TestCase):
	def setUp(self):
		super(StripeTestCase, self).setUp()

		base_url = os.environ.get('PM_API_HOST')
		if api_base:
			stripe.base_url = base_url
		postmaster.config.api_key = os.environ.get('PM_API_KEY', 'tGN0bIwXnHdwOa85VABjPdSn8nWY7G7I')