app.controller("Consumers", ['$rootScope', '$scope', 'Restangular', '$window',
    function($rootScope, $scope, Restangular, $window) {

    var user_details = Restangular.one("users/list/");
    user_details.getList().then(function(consumers) {
        $scope.consumers = consumers;
		console.log('Load consumer from controller!',$scope.consumers);
    }, function(consumers) {
		console.log('Load consumer from controller!',$scope.consumers);
    });        

    }
]);