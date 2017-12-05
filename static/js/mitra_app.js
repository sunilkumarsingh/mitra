var app = angular.module('power-mitra',[
  'infinite-scroll', // This is for scrolling and pagination
	'ui.router',
	'restangular',
	'angular.filter',
	]);

app.run(function($rootScope,Restangular) {

  //set the local time zone offset.
  var tz = jstz.determine();
  var zonename = moment().tz(tz.name()).zoneName();
  $rootScope.localtimezone = ' ('+zonename+')';
  $rootScope.timeformat = 'dd-MMM-yyyy hh:mm:ss a';// format of moment and angular are different.
  $rootScope.currentlocaltime = moment().tz(tz.name()).format('DD-MMM-YYYY hh:mm A')+$rootScope.localtimezone; //'DD-MMM-YYYY hh:mm:ss A zz' current time with zome
  //again reset the header local time zone offset when state changes.
  
  $rootScope.$on('$stateChangeSuccess',
    function(event, toState, toParams, fromState, fromParams, options){
      $rootScope.currentlocaltime = moment().tz(tz.name()).format('DD-MMM-YYYY hh:mm A')+$rootScope.localtimezone;
  });
});

app.config(function( $stateProvider, $urlRouterProvider, RestangularProvider,
	){
	
	RestangularProvider.setRequestSuffix('/');
    RestangularProvider.setDefaultHeaders({"X-CSRFToken" : csrftoken});
	RestangularProvider.addResponseInterceptor(function(data, operation, model, url, response, deferred){

		var extractedData;

		if(operation === "getList")
		{
			console.log(data.results);
			console.log(model);
			console.log(url);
			console.log(response);
			extractedData = data.results;
		}
		else
		{
			extractedData = data;
		}
		return extractedData;
	});

	RestangularProvider.setErrorInterceptor(function(response, deferred, resHandler){
		if(response.status == 403)
		{
			swal({
				title: 'Session Expired',
				text: "You will be logged out.",
				type: 'warning',
				confirmButtonText: "OK",
				confirmButtonClass: 'btn btn-success',
				closeOnConfirm: false,
			}, function(isOk) {
				window.location = '/';
			});
		}
		else{
			console.log("response ", response);
			console.log("deferred ", deferred);
			console.log("resHandler ", resHandler);
		}
	})

	$urlRouterProvider.otherwise('/');

	$stateProvider
		.state('/', {
			url : "/",
			templateUrl : "/static/ng_templates/home.html",
			// controller : "Dashboard"
		})

		.state('dashboard', {
			url : "/dashboard",
			templateUrl : "/static/ng_templates/dashboard.html",
			// controller : "ManageProfile"
		})
		.state('aboutus', {
			url : "/aboutus",
			templateUrl : "/static/ng_templates/aboutus.html",
			// controller : "ManageProfile"
		})
		.state('services', {
			url : "/services",
			templateUrl : "/static/ng_templates/services.html",
			// controller : "ManageProfile"
		})		
		.state('contactus', {
			url : "/contactus",
			templateUrl : "/static/ng_templates/contactus.html",
			// controller : "ContactUs"
		})
		
});
