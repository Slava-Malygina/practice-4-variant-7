class KafkaProducer:
    def send(self, topic: str, value: str):
        pass


class EventPublisher:
    def __init__(self, producer: KafkaProducer):
        self.producer = producer

    def publish_order_created(self, order_id: str, amount: float):
        event = f'{{"type":"OrderCreated","orderId":"{order_id}","amount":{amount}}}'
        self.producer.send("orders", event)