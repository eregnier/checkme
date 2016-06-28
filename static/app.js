var module = angular.module('checkme', []);

module.controller('MainCtrl', function ($scope, $http) {

    $scope.checks = [];
    $scope.text = '';

    $scope.switchCheck = function (check) {
        check.check = !check.check;
        $http.get('/check/check/' + check.id + '/' + (check.check ? 1 : 0));
        console.log('check', check.check);
    };

    $scope.switchCross = function (check) {
        check.cross = !check.cross;
        $http.get('/check/cross/' + check.id + '/' + (check.cross ? 1 : 0 ));
        console.log('cross', check.cross);
    };

    $scope.newCheck = function () {
        $http.get('/check/new/' + $scope.selectedCategory.id + '/' + $scope.text).success(function () {
            $scope.text = '';
            $scope.reloadCheck();
        });
    };

    $scope.reloadCheck = function () {
        $http.get('/check/' + $scope.selectedCategory.id).success(function (data) {
            $scope.checks = data.data;
        });
    };

    $scope.archive = function () {
        $http.get('/check/archive/' + $scope.selectedCategory.id).success(function (data) {
            $scope.checks = data.data;
        });
    };

    $scope.selectCategory = function (category) {
        $scope.selectedCategory = category;
        $scope.reloadCheck();
    };

    $scope.newCategory = function (callback) {
        if ($scope.category) {
            $http.get('/category/new/' + $scope.category).success(function () {
                $scope.reloadCategory();
                $scope.category = '';
            });
        }
    };

    $scope.reloadCategory = function () {
        $http.get('/category/all').success(function (data) {
            $scope.categories = data.data;
            if ($scope.categories.length) {
                $scope.selectedCategory = $scope.categories[0];
                $scope.reloadCheck();
            }
        });
    };

    $scope.changePriority = function(check, priority) {
        check.priority = priority;
        $http.get('/check/priority/' + check.id + '/' + priority);
    };


    $scope.reloadCategory();
});

