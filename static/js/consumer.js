app.controller("Consumers", ['$rootScope', '$scope', 'Restangular', '$window',
    function($rootScope, $scope, Restangular, $window) {
	
	console.log('Load consumer from controller! >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',$rootScope);

	$scope.usersignin = function() {
        var post = {
            'email': $scope.selectedResource.id,
            'password': $scope.password
        }
        var login = Restangular.all("/ajax_login/");
        login.post(post).then(function(user) {
            $scope.user = user;
            $('#loaderbox').hide();
        }, function(timestamps) {
            console.log('error in getting timestamps', timestamps);
        });
	};

    }
]);