""" Stripe payment processing. """
from __future__ import absolute_import, unicode_literals

import logging

import requests, sys
from oscar.apps.payment.exceptions import GatewayError, TransactionDeclined
from oscar.core.loading import get_model

from ecommerce.extensions.payment.processors import (
    BasePaymentProcessor,
    BaseClientSidePaymentProcessor,
    HandledProcessorResponse
)

logger = logging.getLogger(__name__)

BillingAddress = get_model('order', 'BillingAddress')
Country = get_model('address', 'Country')
PaymentEvent = get_model('order', 'PaymentEvent')
PaymentEventType = get_model('order', 'PaymentEventType')
PaymentProcessorResponse = get_model('payment', 'PaymentProcessorResponse')
Source = get_model('payment', 'Source')
SourceType = get_model('payment', 'SourceType')


class Paystack(BaseClientSidePaymentProcessor):
    NAME = 'paystack'
    template_name = 'payment/paystack.html'

    def __init__(self, site):
        """
        Constructs a new instance of the Paystack processor.

        Raises: 
            KeyError: If no settings configured for this payment processor.
        """
        super(Paystack, self).__init__(site)
        configuration = self.configuration
        self.publishable_key = configuration['publishable_key']
        self.secret_key = configuration['secret_key']
        self.country = 'NG' # configuration['country'] #Keeps flagging Key Error problem

    def get_transaction_parameters(self, basket, request=None, use_client_side_checkout=True, **kwargs):
        raise NotImplementedError('The Paystack payment processor does not yet support hosted checkout.')
        # parameters = {
            # 'payment_page_url': 'http://fakeendpoint.com',
        # }
        # return parameters

    def _get_basket_amount(self, basket):
        return str((basket.total_incl_tax * 100).to_integral_value())

    def handle_processor_response(self, response, basket=None):
        token = response
        currency = basket.currency
        res = None
        try:
            headers = {'Authorization': 'Bearer ' + self.secret_key}
            url = 'https://api.paystack.co/transaction/verify/' + token
            req = requests.get(url, headers=headers)
            if req.status_code == 200:
                res = req.json()
                # Validate Amount Paid Here
                if res['data']['status'] == 'success':
                    transaction_id = token #res['data']['trx']
                    self.record_processor_response(res, transaction_id=transaction_id, basket=basket)
                    logger.info('Successfully created Paystack charge [%s] for basket [%d].', transaction_id, basket.id)
                else:
                    base_message = "Paystack payment for basket [%d] declined with HTTP status [%d]"
                    exception_format_string = "{}: %s".format(base_message)
                    self.record_processor_response(res, basket=basket)
                    raise TransactionDeclined(base_message, basket.id, req.status_code)
            else:
                base_message = "Paystack payment for basket [%d] declined with HTTP status [%d] Fake Transaction Token Probably or Payment Gateway is down"
                exception_format_string = "{}: %s".format(base_message)
                body = "Fake Transaction Token"
                logger.exception(
                    exception_format_string,
                    basket.id,
                    req.status_code,
                    body
                )
                self.record_processor_response(body, basket=basket)
                raise TransactionDeclined(base_message, basket.id, req.status_code)
        except:
            base_message = "Paystack payment for basket [%d] declined with HTTP status [%d]"
            exception_format_string = "{}: %s".format(base_message)
            body = sys.exc_info()[0]
            logger.exception(
                exception_format_string,
                basket.id,
                '500',#ex.http_status,
                body
            )
            self.record_processor_response(body, basket=basket)
            raise TransactionDeclined(base_message, basket.id, '500')

        total = basket.total_incl_tax
        card_number = res['data']['authorization']['last4']
        card_type = res['data']['authorization']['brand']

        return HandledProcessorResponse(
            transaction_id=transaction_id,
            total=total,
            currency=currency,
            card_number=card_number,
            card_type=card_type
        )

    def issue_credit(self, order_number, basket, reference_number, amount, currency):
        raise NotImplementedError('The Paystack payment processor does not support transaction parameters.')

    def get_address_from_token(self, token):
        return None