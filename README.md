# Вариант 7: Мокирование очередей сообщений (Kafka / RabbitMQ)

## Контекст
Сервис `EventPublisher` отправляет события в шину (например, Kafka). Запуск брокера в тестах — тяжело и избыточно для unit-тестов.

## Задача
Протестируйте `publish_order_created()`, замокировав `KafkaProducer.send()`.

Требуется проверить:
1. При вызове `publish_order_created("ord_1", 500.0)` метод `producer.send()` вызван **один раз**.  
2. Вызывается с `topic="orders"`.  
3. Тело сообщения — корректный JSON с полями `type`, `orderId`, `amount`.  
4. (Опционально) При исключении в `send()` — оно не подавляется (поведение «fail-fast»).

## Инструменты
- `unittest.mock.Mock`

## Запуск
```bash
pip install -r requirements.txt
pytest tests/ -v