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
        $http.get('/new/check/' + $scope.selectedCategory.id + '/' + $scope.text).success(function () {
            $scope.text = '';
            $scope.reloadCheck();
        });
    };

    $scope.reloadCheck = function () {
        $http.get('/get/check/' + $scope.selectedCategory.id).success(function (data) {
            $scope.checks = data.data;
        });
    };

    $scope.archive = function () {
        $http.get('/archive/' + $scope.selectedCategory.id);
        $scope.reloadCheck();
    };

    $scope.selectCategory = function (category) {
        $scope.selectedCategory = category;
        $scope.reloadCheck();
    };

    $scope.newCategory = function (callback) {
        $http.get('/new/category/' + $scope.category).success(function () {
            $scope.reloadCategory();
            $scope.category = '';
        });
    };

    $scope.reloadCategory = function () {
        $http.get('/get/category').success(function (data) {
            $scope.categories = data.data;
            if ($scope.categories.length) {
                $scope.selectedCategory = $scope.categories[0];
                $scope.reloadCheck();
            }
        });
    };


    $scope.reloadCategory();
});

