/* istanbul ignore next */
require([
    'jquery',
    'payment_processors/rave'
], function($, Rave) {
    'use strict';

    $(document).ready(function() {
        console.log("Rave processor");
        alert("Rave Processor");
        Rave.init(window.RaveConfig);
    });
});
