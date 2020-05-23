""" Stripe payment processing. """
from __future__ import absolute_import, unicode_literals

import logging

from oscar.apps.payment.exceptions import GatewayError, TransactionDeclined
from oscar.core.loading import get_model

from ecommerce.extensions.payment.processors import (
    ApplePayMixin,
    BaseClientSidePaymentProcessor,
    HandledProcessorResponse
)

logger = logging.getLogger(__name__)


class Rave(ApplePayMixin, BaseClientSidePaymentProcessor):
    NAME = 'rave'
    template_name = 'payment/rave.html'

    def __init__(self, site):
        """
        Constructs a new instance of the Stripe processor.

        Raises:
            KeyError: If no settings configured for this payment processor.
        """
        super(Paystack, self).__init__(site)
        configuration = self.configuration
        self.publishable_key = configuration['publishable_key']
        self.secret_key = configuration['secret_key']

    def get_transaction_parameters(self, basket, request=None, use_client_side_checkout=True, **kwargs):
        raise NotImplementedError('The Paystack payment processor does not support transaction parameters.')

    def _get_basket_amount(self, basket):
        return str((basket.total_incl_tax * 100).to_integral_value())

    def handle_processor_response(self, response, basket=None):
        token = response
        order_number = basket.order_number
        currency = basket.currency

        # try:
        #     charge = stripe.Charge.create(
        #         amount=self._get_basket_amount(basket),
        #         currency=currency,
        #         source=token,
        #         description=order_number,
        #         metadata={'order_number': order_number}
        #     )
        #     transaction_id = charge.id

        #     # NOTE: Charge objects subclass the dict class so there is no need to do any data transformation
        #     # before storing the response in the database.
        #     self.record_processor_response(charge, transaction_id=transaction_id, basket=basket)
        #     logger.info('Successfully created Stripe charge [%s] for basket [%d].', transaction_id, basket.id)
        # except stripe.error.CardError as ex:
        #     base_message = "Stripe payment for basket [%d] declined with HTTP status [%d]"
        #     exception_format_string = "{}: %s".format(base_message)
        #     body = ex.json_body
        #     logger.exception(
        #         exception_format_string,
        #         basket.id,
        #         ex.http_status,
        #         body
        #     )
        #     self.record_processor_response(body, basket=basket)
        #     raise TransactionDeclined(base_message, basket.id, ex.http_status)

        # total = basket.total_incl_tax
        # card_number = charge.source.last4
        # card_type = STRIPE_CARD_TYPE_MAP.get(charge.source.brand)

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
        raise NotImplementedError('The Paystack payment processor does not support get_address_from_token.')
