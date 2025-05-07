import json
from typing import Dict, Any
from fastapi import Depends, HTTPException

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

from ... import logger, settings


class KafkaProducerService:
    def __init__(self, bootstrap_servers: list[str] = []):
        self.bootstrap_servers = bootstrap_servers if len(bootstrap_servers) else [settings.BOOTSTRAP_SERVERS]
        self.producer = None

    async def get_producer(self) -> AIOKafkaProducer:
        if self.producer is None:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all'

            )
            await self.producer.start()
        return self.producer

    async def send_message(self, topic: str, key: str, value: Dict[str, Any]) -> Dict[str, Any]:
        producer = await self.get_producer()

        try:
            result = await producer.send_and_wait(
                topic=topic,
                key=key,
                value=value,
            )
            return {
                "status": "sent",
                "topic": topic,
                "partition": result.partition,
                "offset": result.offset
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

    async def close(self):
        if self.producer is not None:
            await self.producer.stop()
