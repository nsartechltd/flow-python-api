from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..middleware.stripe import stripe_webhook_verifier

router = APIRouter()

class StripeWebhookRequestBody(BaseModel):
  type: str

@router.post('/webhook', dependencies=[Depends(stripe_webhook_verifier)])
async def stripe_webhook(body: StripeWebhookRequestBody):
  return body