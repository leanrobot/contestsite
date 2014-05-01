DEBUG = 0
test = true

angularApp = angular.module "Grading", ['ngSanitize']
	.config ($interpolateProvider) -> 
		$interpolateProvider.startSymbol('[[');
		$interpolateProvider.endSymbol(']]');

angularApp.factory "api", ($http, $q) ->
		return {
			test: ->
				console.log "test!"
			getUngradedResults: (successFunc) ->
				console.log()
				$http.get('/api/v1/ungradedresult?format=json')
				.then successFunc,
				(response) ->
					return $q.reject response.data 
		}


angularApp.controller 'Main',
		class GradingMain
			# @$inject: [, '$scope']
			constructor: (@$scope, @api) ->
				DEBUG = @
				console.log "controller: create"
				@$scope.solutions = []
				@$scope.solution = null
				@load()

				@$scope.jscode = 
				"""
				var j = 5;
				var x = 6;
				alert("hello!");
				"""

				@time = new TimeConversion()
			
			load: -> 
				console.log "controller: load"
				@$scope.loading = true
				@api.getUngradedResults (response) => 
					console.log "graded results: "
					console.log response.data.objects
					@$scope.solutions = response.data.objects
					@$scope.loading = false

			setSelected: (solution) ->
				console.log "controller: select"
				console.log solution
				@$scope.solution = solution

			highlightCode: (code) ->
				if code?
					console.log "highlight"
					return hljs.highlightAuto(code).value
				else 
					console.log "no highlight"
					return ''

			runningTime: (startraw, endraw) ->
				console.log @time
				start = @time?.createTime startraw
				end = @time?.createtime endraw
				#diff = end - start

				return diff



class TimeConversion
	constructor: () ->

	createTime: (timeraw) ->
		date = new Date(timeraw)

	millisToSeconds: (millis, accuracy=1) ->
		#seconds = math.floor(millis / 1000)
		#remainder = ((float)millis) - (seconds * 1000)
		###
		52,451
		52.451
		x / 10
		###