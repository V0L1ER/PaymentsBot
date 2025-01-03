import os
from dotenv import load_dotenv
from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, LabeledPrice, ContentType, PreCheckoutQuery

import keyboards.inline_kb as in_kb

router = Router()
load_dotenv()

PRICE = LabeledPrice(label="Подписка на 1 месяц", amount=500*100)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет')
    
@router.message(Command('subscribe'))
async def cmd_start(message: Message, bot: Bot):
    if os.getenv("PAYMENTS_TOKEN").split(':')[1] == 'TEST':
        await message.answer("Тестовый платеж!")
        
    await bot.send_invoice(message.chat.id,
                        title="Подписка на бота",
                        description="Активация подписки на бота на 1 месяц",
                        provider_token=os.getenv("PAYMENTS_TOKEN"),
                        currency="rub",
                        photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                        photo_width=416,
                        photo_height=234,
                        photo_size=416,
                        is_flexible=False,
                        prices=[PRICE],
                        start_parameter="one-month-subscription",
                        payload="test-invoice-payload"
                        )
    
@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout: PreCheckoutQuery):
    await pre_checkout.answer(ok=True)
    
    
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def succsecful_payment(message: Message):
    print("SUCCESSFUL PAYMENT")
    payment_info = message.successful_payment
    
    print(f"Invoice payload: {payment_info.invoice_payload}")
    print(f"Total amount: {payment_info.total_amount}")
    print(f"Currency: {payment_info.currency}")
 
    await message.answer(f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
    
                        
    
    

