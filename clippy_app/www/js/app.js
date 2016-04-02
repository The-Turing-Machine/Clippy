// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
var App = angular.module('starter', ['ionic']);

App.service("imdb",["$http","$log",imdb]);
angular.module('services', [])
.service('UserService', function() {
  // For the purpose of this example I will store user data on ionic local storage but you should save it on a database

  var setUser = function(user_data) {
    window.localStorage.starter_google_user = JSON.stringify(user_data);
  };

  var getUser = function(){
    return JSON.parse(window.localStorage.starter_google_user || '{}');
  };

  return {
    getUser: getUser,
    setUser: setUser
  };
});


App.controller("AppCtrl",["$scope","$log","imdb",AppCtrl]);

/*function AppCtrl($scope,$log,imdb){

  $scope.data = [];
  $scope.refresh = function(d){
    console.log(d);
    var d = (d.split(" ")).join("+") ;
       console.log(d);
  imdb.getmovie($scope,d);

}

}*/
/*function imdb($http,$log){
  d = []
  this.getmovie = function($scope,d){
    $http.jsonp("http://www.omdbapi.com/?s="+d+"&callback=JSON_CALLBACK")
    .success(function(result){

      $scope.data = result.Search;
      $scope.$broadcast("scroll.refreshComplete");
      $log.info(JSON.stringify(result.Search));

    });
  };
}*/

function AppCtrl($scope,$log,imdb){

  $scope.data = [];
  $scope.refresh = function(d){
    console.log(d);
    var d = (d.split(" ")).join("+") ;
       console.log(d);
  imdb.getmovie($scope,d);

}

}


function imdb($http,$log){
  d = []
  this.getmovie = function($scope,d){
    $http.jsonp("http://api.themoviedb.org/3/search/movie?api_key=d40f8d561eedf9402a64cfb304c27dc1&query="+d+"&callback=JSON_CALLBACK")
    .success(function(result){
      
      for(var i=0;i<result.results.length;i++)
      {
        result.results[i]["poster_path"] = "http://image.tmdb.org/t/p/w500" + result.results[i]["poster_path"]
      }
      $scope.data = result.results;
      
      $scope.$broadcast("scroll.refreshComplete");
      $log.info(JSON.stringify(result.results));

    });
  };


}















/*apikey=6341e4e4*/ 
App.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if(window.cordova && window.cordova.plugins.Keyboard) {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

      // Don't remove this line unless you know what you are doing. It stops the viewport
      // from snapping when text inputs are focused. Ionic handles this internally for
      // a much nicer keyboard experience.
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
})



App.controller('WelcomeCtrl', function($scope, $state, UserService, $ionicLoading) {
  // This method is executed when the user press the "Sign in with Google" button
  $scope.googleSignIn = function() {
    $ionicLoading.show({
      template: 'Logging in...'
    });

    window.plugins.googleplus.login(
      {},
      function (user_data) {
        // For the purpose of this example I will store user data on local storage
        UserService.setUser({
          userID: user_data.userId,
          name: user_data.displayName,
          email: user_data.email,
          picture: user_data.imageUrl,
          accessToken: user_data.accessToken,
          idToken: user_data.idToken
        });

        $ionicLoading.hide();
        $state.go('app.home');
      },
      function (msg) {
        $ionicLoading.hide();
      }
    );
  };
})



