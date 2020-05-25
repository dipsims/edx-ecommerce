/* istanbul ignore next */
require([
    'jquery',
    'payment_processors/paystack'
], function($, PaystackProcessor) {
    'use strict';

    $(document).ready(function() {
        var scriptElem = document.createElement('script');
        scriptElem.setAttribute('src', 'https://js.paystack.co/v2/popup.js');
        scriptElem.setAttribute('type','text/javascript');
        document.getElementsByTagName('head')[0].appendChild(scriptElem);
        PaystackProcessor.init(window.PaystackConfig);
    });
});
