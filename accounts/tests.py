from django.test import TestCase

from accounts.views import TeamLoginRequiredMixin, JudgeLoginRequiredMixin

import testing.control as control

class TestTeamLoginRequiredMixin(TestCase):
	def setUp(self):
		self.team = control.create_team()
		self.judge = control.create_judge()
		self.staff = control.create_staff()

		self.view = TeamLoginRequiredMixin()

	def test_is_team_user(self):
		""" Tests with team, judge and staff user to make sure that only team
			and staff return true.
		"""
		assert self.view.is_team_user(self.team), """
			team should be allowed to access, expected true, got false """

		assert not self.view.is_team_user(self.judge), """
			judge should not be allowed to access, expected false, got true """

		assert self.view.is_team_user(self.staff), """
			staff should be allowed to access, expected true, got false """

class TestJudgeLoginRequiredMixin(TestCase):
	def setUp(self):
		self.team = control.create_team()
		self.judge = control.create_judge()
		self.staff = control.create_staff()

		self.view = JudgeLoginRequiredMixin()

	def test_is_judge_user(self):
		""" Tests with team, judge and staff user to make sure that only judge
			and staff return true.
		"""
		assert self.view.is_judge_user(self.judge), """
			team should be allowed to access, expected true, got false """

		assert not self.view.is_judge_user(self.team), """
			judge should not be allowed to access, expected false, got true """

		assert self.view.is_judge_user(self.staff), """
			staff should be allowed to access, expected true, got false """
