/**
 * Paystack payment processor specific actions.
 */
define([
    'jquery',
    'underscore.string'
], function($, _s) {
    'use strict';

    return {
        init: function(config) {
            this.publishableKey = config.publishableKey;
            this.postUrl = config.postUrl;
            this.$paymentForm = $('#paymentForm');
            this.$paymentButton = $('#payment-request-button-paystack');
            this.paymentRequestConfig = {
                country: config.country,
                email: config.paymentRequest.email,
                currency: config.paymentRequest.currency,
                total: {
                    label: config.paymentRequest.label,
                    amount: config.paymentRequest.total
                }
            };

            this.$paymentForm.on('submit', $.proxy(this.onPaymentFormSubmit, this));
            this.$paymentButton.on('click', $.proxy(this.onPaymentFormSubmit, this));
            this.initializePaymentRequest();
        },

        onPaymentFormSubmit: function(evt) {
            evt.preventDefault();
            var self = this;
            var handler = PaystackPop.setup({
                key: this.publishableKey,
                email: this.paymentRequestConfig.email,
                amount: this.paymentRequestConfig.total.amount,
                metadata: {
                custom_fields: [
                    {
                        label: this.paymentRequestConfig.total.label,
                        country: this.paymentRequestConfig.country
                    }
                ]},
                callback: function(token) {
                    var formData = new FormData();
                    formData.append('paystack_token', token.reference);
                    formData.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]', self.$paymentForm).val());
                    formData.append('basket', $('[name=basket]', self.$paymentForm).val());
                    console.log("Start Loader");
                    fetch(self.postUrl, {
                        credentials: 'include',
                        method: 'POST',
                        body: formData
                    }).then(function(response) {
                        console.log("Stop Loader");
                        if (response.ok) {
                            response.json().then(function(data) {
                                window.location.href = data.url;
                            });
                        } else {
                            self.displayErrorMessage(gettext('An error occurred while processing your payment. ' +
                                'Please try again.'));
                        }
                    });
                },
                onClose: function(){
                    // NOP
                }
            });
            handler.openIframe();
        },

        displayErrorMessage: function(message) {
            $('#messages').html(
                _s.sprintf(
                    '<div class="alert alert-error"><i class="icon fa fa-exclamation-triangle"></i>%s</div>',
                    message
                )
            );
        },

        initializePaymentRequest: function() {
            //Create Pay With Pay Stack Button in #payment-request-button-paystack
            $('#payment-request-button-paystack')
            .html('<a href="#payment-information" class="payment-button credit-card" title="Pay with Paystack" role="button"><img src="/static/images/paystack.png"></a>');
        }
    };
});
