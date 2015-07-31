var app = angular.module("SteerClear", ['angularReverseGeocode']).config(function($interpolateProvider){
	//This line is meant to resolve a conflict with Jinja 2, which also uses the double
	//braces {{}}. This replaces the method for angular binding from {{}} to {[{}]}.
	$interpolateProvider.startSymbol('{[{').endSymbol('}]}');
})