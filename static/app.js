var module = angular.module('checkme', []);

module.controller('MainCtrl', function ($scope, $http) {

    $scope.checks = [];
    $scope.text = '';

    $scope.switchCheck = function (check) {
        check.check = !check.check;
        $http.get('/check/' + check.id + '/' + (check.check ? 1 : 0));
        console.log('check', check.check);
    };

    $scope.switchCross = function (check) {
        check.cross = !check.cross;
        $http.get('/cross/' + check.id + '/' + (check.cross ? 1 : 0 ));
        console.log('cross', check.cross);
    };

    $scope.newCheck = function () {
        $http.get('/new/' + $scope.text).success(function () {
            $scope.reload();
            $scope.text = '';
        });
    };

    $scope.reload = function () {
        $http.get('/get').success(function (data) {
            $scope.checks = data.data;
        });
    }

    $scope.archive = function () {
        $http.get('/archive');
        $scope.reload();
    };

    $scope.reload();
});

