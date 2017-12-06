app.controller("Consumers", ['$rootScope', '$scope', 'Restangular', '$window',
    function($rootScope, $scope, Restangular, $window) {

    var latest_run = Restangular.all("users/list/");
    console.log('Load consumer from controller!',latest_run);

    var user_details = Restangular.one("users/list/");
    user_details.get().then(function(consumers) {
        // consumers.put();
        $scope.consumers = consumers;
		console.log('Load consumer from controller!',consumers);
    }, function(consumers) {
		console.log('Load consumer from controller!',consumers);
    });        

    }
]);