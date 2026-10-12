import json
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from service import EventPublisher


def test_publish_order_created_sends_correct_event():
    mock_producer = Mock()
    publisher = EventPublisher(mock_producer)

    publisher.publish_order_created("ord_1", 500.0)

    mock_producer.send.assert_called_once()

    args, kwargs = mock_producer.send.call_args
    assert kwargs == {}
    assert len(args) == 2

    topic, raw_payload = args

    assert topic == "orders"

    assert isinstance(raw_payload, str)
    event = json.loads(raw_payload)

    assert event == {
        "type": "OrderCreated",
        "orderId": "ord_1",
        "amount": 500.0,
    }
    assert isinstance(event["amount"], float)


def test_publish_order_created_does_not_suppress_send_exception():
    mock_producer = Mock()
    mock_producer.send.side_effect = RuntimeError("Kafka unavailable")

    publisher = EventPublisher(mock_producer)

    with pytest.raises(RuntimeError, match="Kafka unavailable"):
        publisher.publish_order_created("ord_1", 500.0)

    mock_producer.send.assert_called_once()

    args, kwargs = mock_producer.send.call_args
    assert args[0] == "orders"
    assert json.loads(args[1])["orderId"] == "ord_1"