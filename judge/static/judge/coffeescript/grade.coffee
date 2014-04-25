DEBUG = 0

angularApp = angular.module "Grading", []
	.config ($interpolateProvider) -> 
		$interpolateProvider.startSymbol('[[');
		$interpolateProvider.endSymbol(']]');

angularApp.factory "api", ($http, $q) ->
		return {
			test: ->
				console.log "test!"
			getUngradedResults: (successFunc) ->
				$http.get('/api/v1/ungradedresult?format=json')
				.then successFunc,
				(response) ->
					return $q.reject response.data 
		}

angularApp.controller 'Main',
		class GradingMain
			# @$inject: [, '$scope']
			constructor: (@$scope, @api) ->
				console.log "instantiated"
				@$scope.solutions = [{command:'test'}, {command:'test234'}]
				@load()
			
			load: -> 
				console.log "load called"
				@api.getUngradedResults (response) => 
					console.log(response.data.objects)
					@$scope.solutions = response.data.objects
					DEBUG = @solutions

			setSelected: (solution) ->
				console.log "selected!"
				console.log solution

