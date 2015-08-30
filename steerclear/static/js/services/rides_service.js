app.service("RidesService", ['$http', '$q', function( $http, $q ) {

    //Make the following methods public
    return({
        createRide: createRide,
        getRides: getRides,
        getRide: getRide,
        deleteRide: deleteRide,
        notify: notify
    });
    // ---
    // PUBLIC METHODS.
    // ---

    function createRide( ride_info ) {
        var request = $http({
            method: "post",
            url: "api/rides",
            data: ride_info
        });
        return( request.then( handleSuccess, handleError ) );
    }

    function getRides() {
        var request = $http({
            method: "get",
            url: "api/rides",
        });
        return( request.then( handleSuccess, handleError ) );
    }
    function getRide( ride_id ) {
        var request = $http({
            method: "get",
            url: "api/rides/" + ride_id,
        });
        return( request.then( handleSuccess, handleError ) );
    }

    function notify( ride_id ) {
        var request = $http({
            method: "post",
            url: "api/notifications/" + ride_id,
        });
        return( request.then( handleSuccess, handleError ) );
    }

    function deleteRide( ride_id ) {
        var request = $http({
            method: "delete",
            url: "api/rides/" + ride_id,
        });
        return( request.then( handleSuccess, handleError ) );
    }

    // ---
    // PRIVATE METHODS.
    // ---
    // Transform the error response, unwrapping the application dta from
    // the API response payload.
    function handleError( response ) {

        if ( ! angular.isObject( response.data ) || ! response.data.message) {
            return( $q.reject( "An unknown error occurred." ) );
        }
        //Return an error message if there is one
        return( $q.reject( response.data.message ) );
    }
    // I transform the successful response, unwrapping the application data
    // from the API response payload.
    function handleSuccess( response ) {
        return( response.data );
    }

}]);
