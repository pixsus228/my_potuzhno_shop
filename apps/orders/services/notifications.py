
class TelegramService:
    @staticmethod
    def send_order_notification(order):
        # В майбутньому сюди додамо TOKEN вашого бота
        message = f'🚀 НОВЕ ЗАМОВЛЕННЯ #{order.id}\\n👤 Клієнт: {order.customer_name}\\n📞 Тел: {order.phone}\\n📍 Місто: {order.city}\\n📮 Пошта: {order.post_office}\\n💰 Сума: {order.total_price} грн.'
        print(f'--- ТЕЛЕГРАМ ПОВІДОМЛЕННЯ: --- \\n{message}')
        # requests.post(f'https://api.telegram.org/botTOKEN/sendMessage', data={{'chat_id': 'CHAT_ID', 'text': message}})
