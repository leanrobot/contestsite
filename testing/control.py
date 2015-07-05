from __future__ import absolute_import
from datetime import datetime, date, timedelta

from django.contrib.auth.models import User, Group
import django.contrib.auth.hashers as hasher
from django.conf import settings

from control.models import ContestSettings
from team.models import UserSettings
from problems.models import Problem

DEFAULT_PASSWORD = "password"

 #  _____       _     _ _        __  __      _   _               _     
 # |  __ \     | |   | (_)      |  \/  |    | | | |             | |    
 # | |__) |   _| |__ | |_  ___  | \  / | ___| |_| |__   ___   __| |___ 
 # |  ___/ | | | '_ \| | |/ __| | |\/| |/ _ \ __| '_ \ / _ \ / _` / __|
 # | |   | |_| | |_) | | | (__  | |  | |  __/ |_| | | | (_) | (_| \__ \
 # |_|    \__,_|_.__/|_|_|\___| |_|  |_|\___|\__|_| |_|\___/ \__,_|___/

def set_contest_in_session():
	dt = timedelta(days=1)
	start_time = datetime.now() - dt
	end_time = datetime.now() + dt
	contest_settings = ContestSettings(startTime=start_time, endTime=end_time,
		name="test contest", deduction = 0)
	contest_settings.save()

def set_contest_not_in_session():
	start_time = now() + timedelta(days=10)
	end_time = now() + timedelta(days=11)
	contest_settings = ContestSettings(startTime=start_time, endTime=end_time,
		name="test contest", deduction = 0)
	contest_settings.save()

def create_team(username="team"):
	_create_groups()
	team = User(username=username, 
		password=hasher.make_password(DEFAULT_PASSWORD))
	team.save()

	user_settings = UserSettings(teamName=username, user=team)
	user_settings.save()

	team_group = Group.objects.get(name=settings.TEAM_GROUP_NAME)
	team_group.user_set.add(team)

	return team

def create_judge(username="judge"):
	_create_groups()
	judge = User(username=username, 
		password=hasher.make_password(DEFAULT_PASSWORD))
	judge.save()

	user_settings = UserSettings(teamName=username, user=judge)
	user_settings.save()

	judge_group = Group.objects.get(name=settings.JUDGE_GROUP_NAME)
	judge_group.user_set.add(judge)

	return judge

def create_staff(username="staff"):
	_create_groups()
	staff = User(username=username, is_staff=True,
		password=hasher.make_password(DEFAULT_PASSWORD))
	staff.save()

	user_settings = UserSettings(teamName=username, user=staff)
	user_settings.save()

	return staff

def create_problem(**kwargs):
	problem = Problem(**kwargs)
	problem.save()
	return problem

 #  _____      _            _         __  __      _   _               _     
 # |  __ \    (_)          | |       |  \/  |    | | | |             | |    
 # | |__) | __ ___   ____ _| |_ ___  | \  / | ___| |_| |__   ___   __| |___ 
 # |  ___/ '__| \ \ / / _` | __/ _ \ | |\/| |/ _ \ __| '_ \ / _ \ / _` / __|
 # | |   | |  | |\ V / (_| | ||  __/ | |  | |  __/ |_| | | | (_) | (_| \__ \
 # |_|   |_|  |_| \_/ \__,_|\__\___| |_|  |_|\___|\__|_| |_|\___/ \__,_|___/

def _create_groups():
	""" Creates the required groups: team and judge used for the auth
		system if they don't already exist.
	"""
	if not Group.objects.filter(name=settings.TEAM_GROUP_NAME).exists():
		team_group = Group(name=settings.TEAM_GROUP_NAME)
		team_group.save()

	if not Group.objects.filter(name=settings.JUDGE_GROUP_NAME).exists():
		judge_group = Group(name=settings.JUDGE_GROUP_NAME)
		judge_group.save()
