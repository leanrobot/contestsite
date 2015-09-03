DEBUG = 0
test = true

angularApp = angular.module "Grading", ['ngSanitize', 'ngResource']
	.config ($interpolateProvider) -> 
		$interpolateProvider.startSymbol('[[');
		$interpolateProvider.endSymbol(']]');

###
angularApp.config ($resourceProvider) ->
		# Don't strip trailing slashes from calculated URLs
		$resourceProvider.defaults.stripTrailingSlashes = false;
###

angularApp.factory "api", ($http, $q, $resource) ->
		return {
			test: ->
				console.log "test!"
			getUngradedResults: (successFunc) ->
				console.log()
				$http.get('/api/v1/ungradedresult?format=json')
				.then successFunc,
				(response) ->
					return $q.reject response.data 
			gradeResult: (correct, solution, successFunc) ->
				solution.graded = true
				solution.successful = correct
				console.log solution.id
				$http {
						url: "/api/v1/problemresult/#{solution.id}/?format=json"
						data: solution
						method: "PATCH"
					}
				.then successFunc
		}


angularApp.controller 'Main',
		class GradingMain
			# @$inject: [, '$scope']
			constructor: (@$scope, @api) ->
				DEBUG = @
				console.log "controller: create"
				@$scope.solutions = []
				@$scope.selected = null
				@load()

				@time = new TimeConversion()
			
			load: -> 
				console.log "controller: load"
				@$scope.selected = null
				@$scope.loading = true
				@api.getUngradedResults (response) => 
					console.log "graded results: "
					console.log response.data.objects
					@$scope.solutions = response.data.objects
					if @$scope.solutions.length > 0
						@$scope.selected = @$scope.solutions[0]
					@$scope.loading = false

			gradeResult: (correct, solution) ->
				@$scope.solutions = []
				@api.gradeResult correct, solution, (response) =>
					@$scope.selected = null
					@load()

			setSelected: (solution) ->
				console.log "controller: select"
				console.log solution
				@$scope.selected = solution

			highlightCode: (code) ->
				if code?
					highlightObj = hljs.highlightAuto code
					return highlightObj.value
				else 
					return code

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