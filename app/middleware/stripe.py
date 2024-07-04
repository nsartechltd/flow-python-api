from fastapi import status, HTTPException, Request
from stripe import stripe
from typing_extensions import Annotated
import os

from ..utils.logger import logger

stripe.api_key = os.environ['STRIPE_API_KEY']

async def stripe_webhook_verifier(request: Request):
  signature = request.headers.get('stripe-signature')
  body = await request.body()

  logger.info(body)

  logger.info('Stripe signature header received')
  logger.info(signature)

  if not signature:
    logger.error('Stripe signature header not present')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No stripe signature header present')

  secret = os.environ['STRIPE_WEBHOOK_SECRET']

  try:
    stripe.Webhook.construct_event(payload=body, sig_header=signature, secret=secret)
  except ValueError as e:
    logger.error(e)
    raise HTTPException(status_code=400, detail='Invalid payload')
  except stripe.error.SignatureVerificationError as e:
    logger.error(e)
    raise HTTPException(status_code=400, detail='Invalid payload')