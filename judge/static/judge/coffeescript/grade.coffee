

angularApp = angular.module("Grading", []);

angularApp.config ($interpolateProvider) -> 
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');

angularApp.controller 'Main',
	class GradingMain
		constructor: (@$scope) ->
			console.log "instantiated"

		solutions: [
			{name:"test"}
			{name:"test2"}
		]
			

		setSelected: ->
			alert "selected!"