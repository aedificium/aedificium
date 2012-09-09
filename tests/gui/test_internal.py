# ###################################################
# Copyright (C) 2012 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

from tests.gui import gui_test, TestFinished


@gui_test(use_dev_map=True)
def test_trivial(gui):
	"""Does nothing to see if test setup works."""
	yield TestFinished


@gui_test(use_fixture='boatbuilder')
def test_trigger(gui):
	"""Test the different ways to trigger an action in a gui."""
	yield

	assert not gui.find('captains_log')

	# Specify event name and group name
	gui.trigger('mainhud', 'logbook/action/default')
	assert gui.find('captains_log')
	gui.trigger('captains_log', 'okButton/action/default')
	assert not gui.find('captains_log')

	# Leave out group name
	gui.trigger('mainhud', 'logbook/action')
	assert gui.find('captains_log')
	gui.trigger('captains_log', 'okButton/action')
	assert not gui.find('captains_log')

	# Leave out event name
	gui.trigger('mainhud', 'logbook')
	assert gui.find('captains_log')
	gui.trigger('captains_log', 'okButton')
	assert not gui.find('captains_log')

	# Select mainsquare and show production overview to test
	# if mouseClicked and action are handled the same
	assert not gui.find('production_overview')

	gui.cursor_click(53, 12, 'left')
	gui.trigger('tab_account', 'show_production_overview/mouseClicked')
	assert gui.find('production_overview')
	gui.trigger('production_overview', 'okButton/action')
	assert not gui.find('production_overview')

	# Leave out event name, it will try action at first and fallback
	# to mouseClicked
	gui.trigger('tab_account', 'show_production_overview')
	assert gui.find('production_overview')
	gui.trigger('production_overview', 'okButton')
	assert not gui.find('production_overview')

	yield TestFinished


@gui_test(timeout=60)
def test_dialog(gui):
	"""Test handling of a dialog."""
	yield

	assert not gui.find('help_window')

	def func():
		yield
		assert gui.find('help_window')
		gui.trigger('help_window', 'okButton/action/__execute__')

	with gui.handler(func):
		gui.trigger('menu', 'helpLink')

	assert not gui.find('help_window')

	yield TestFinished
