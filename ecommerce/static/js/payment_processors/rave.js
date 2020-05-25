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
            this.paymentRequestConfig = {
                country: config.country,
                currency: config.paymentRequest.currency,
                total: {
                    label: config.paymentRequest.label,
                    amount: config.paymentRequest.total
                }
            };
            alert("Rave");
            console.log("Rave");
            // this.$paymentForm.on('submit', $.proxy(this.onPaymentFormSubmit, this));
            // this.initializePaymentRequest();
        },

        onPaymentFormSubmit: function(evt) {
            // self.postTokenToServer(ev.token.id, ev);
            // evt.preventDefault();
            // var handler = PaystackPop.setup({
            //     key: '{{ client_side_payment_processor.publishable_key }}',
            //     email: 'dretnan@logicaladdress.com',
            //     amount: {% widthratio order_total.incl_tax 1 (100 * 360) %},
            //     metadata: {
            //     custom_fields: [
            //         {
            //             label: "{{ platform_name }}",
            //             country: "{{ client_side_payment_processor.country }}"
            //         }
            //     ]
            //     },
            //     callback: self.postTokenToServer,
            //     onClose: function(){
            //         alert('window closed');
            //     }
            // });
            // handler.openIframe();
        },

        postTokenToServer: function(token, paymentRequest) {
            var self = this,
                formData = new FormData();

            formData.append('paystack_token', token);
            formData.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]', self.$paymentForm).val());
            formData.append('basket', $('[name=basket]', self.$paymentForm).val());

            fetch(self.postUrl, {
                credentials: 'include',
                method: 'POST',
                body: formData
            }).then(function(response) {
                if (response.ok) {
                    if (paymentRequest) {
                        // Report to the browser that the payment was successful, prompting
                        // it to close the browser payment interface.
                        paymentRequest.complete('success');
                    }
                    response.json().then(function(data) {
                        window.location.href = data.url;
                    });
                } else {
                    if (paymentRequest) {
                        // Report to the browser that the payment failed, prompting it to re-show the payment
                        // interface, or show an error message and close the payment interface.
                        paymentRequest.complete('fail');
                    }

                    self.displayErrorMessage(gettext('An error occurred while processing your payment. ' +
                        'Please try again.'));
                }
            });
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
            // this.paymentRequestConfig
            //Create Pay With Pay Stack Button here
        }
    };
});
