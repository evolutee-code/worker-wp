import json
from typing import Dict, Any, List
from fastapi import Depends, HTTPException

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

from ... import settings


class KafkaConsumerService:
    def __init__(self, bootstrap_servers: list[str] = []):
        self.bootstrap_servers = bootstrap_servers if len(bootstrap_servers) else [settings.BOOTSTRAP_SERVERS]
        self.consumers = {}

    async def create_consumer(self, topic: str, group_id: str) -> AIOKafkaConsumer:
        consumer_key = f"{topic}_{group_id}"

        if consumer_key not in self.consumers:
            consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
                auto_offset_reset='earliest'
            )
            await consumer.start()
            self.consumers[consumer_key] = consumer

        return self.consumers[consumer_key]

    async def consume_messages(self, topic: str, group_id: str, max_messages: int = 10) -> List[Dict[str, Any]]:
        consumer = await self.create_consumer(topic, group_id)

        messages = []
        try:
            # Poll with timeout
            async for msg in consumer:
                messages.append({
                    "topic": msg.topic,
                    "partition": msg.partition,
                    "offset": msg.offset,
                    "key": msg.key,
                    "value": msg.value,
                    "timestamp": msg.timestamp
                })

                if len(messages) >= max_messages:
                    break

            return messages
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to consume messages: {str(e)}")

    async def close(self):
        for consumer in self.consumers.values():
            await consumer.stop()
