// Generated by CoffeeScript 1.7.1
var DEBUG, GradingMain, TimeConversion, angularApp, test;

DEBUG = 0;

test = true;

angularApp = angular.module("Grading", ['ngSanitize']).config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  return $interpolateProvider.endSymbol(']]');
});

angularApp.factory("api", function($http, $q) {
  return {
    test: function() {
      return console.log("test!");
    },
    getUngradedResults: function(successFunc) {
      console.log();
      return $http.get('/api/v1/ungradedresult?format=json').then(successFunc, function(response) {
        return $q.reject(response.data);
      });
    }
  };
});

angularApp.controller('Main', GradingMain = (function() {
  function GradingMain($scope, api) {
    this.$scope = $scope;
    this.api = api;
    DEBUG = this;
    console.log("controller: create");
    this.$scope.solutions = [];
    this.$scope.solution = null;
    this.load();
    this.$scope.jscode = "var j = 5;\nvar x = 6;\nalert(\"hello!\");";
    this.time = new TimeConversion();
  }

  GradingMain.prototype.load = function() {
    console.log("controller: load");
    this.$scope.loading = true;
    return this.api.getUngradedResults((function(_this) {
      return function(response) {
        console.log("graded results: ");
        console.log(response.data.objects);
        _this.$scope.solutions = response.data.objects;
        return _this.$scope.loading = false;
      };
    })(this));
  };

  GradingMain.prototype.setSelected = function(solution) {
    console.log("controller: select");
    console.log(solution);
    return this.$scope.solution = solution;
  };

  GradingMain.prototype.highlightCode = function(code) {
    var highlightObj;
    if (code != null) {
      highlightObj = hljs.highlightAuto(code);
      return highlightObj.value;
    } else {
      return code;
    }
  };

  GradingMain.prototype.runningTime = function(startraw, endraw) {
    var end, start, _ref, _ref1;
    console.log(this.time);
    start = (_ref = this.time) != null ? _ref.createTime(startraw) : void 0;
    end = (_ref1 = this.time) != null ? _ref1.createtime(endraw) : void 0;
    return diff;
  };

  return GradingMain;

})());

TimeConversion = (function() {
  function TimeConversion() {}

  TimeConversion.prototype.createTime = function(timeraw) {
    var date;
    return date = new Date(timeraw);
  };

  TimeConversion.prototype.millisToSeconds = function(millis, accuracy) {
    if (accuracy == null) {
      return accuracy = 1;
    }

    /*
    		52,451
    		52.451
    		x / 10
     */
  };

  return TimeConversion;

})();
