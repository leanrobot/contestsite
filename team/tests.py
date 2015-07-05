from __future__ import absolute_import

from django.test import TestCase
from django.core.urlresolvers import reverse

import testing.view_access as view_access
import testing.control

class TestProblemListView(TestCase):
	def setUp(self):
		testing.control.set_contest_in_session()

	def test_view_exists(self):
		team_user= testing.control.create_team()
		status = view_access.get(view_name="problem list", user=team_user)
		assert status == 200, "Expected 200 for view, got %d" % status

class TestProblemDetailView(TestCase):
	def setUp(self):
		testing.control.set_contest_in_session()
		self.problem = testing.control.create_problem(name="test problem", score=10)

	def test_view_exists(self):
		team_user= testing.control.create_team()
		url = reverse("problem detail", args=[self.problem.id])
		status = view_access.get(view_url=url, user=team_user)
		assert status == 200, "Expected 200 for view, got %d" % status



