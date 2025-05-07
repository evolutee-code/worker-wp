from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

from ...configs import settings
from ...exceptions import HTTP_201_CREATED, HTTP_302_FOUND


class KafkaAdminService:
    bootstrap_servers: list[str]

    def __init__(self, bootstrap_servers: list[str] = []):
        self.bootstrap_servers = bootstrap_servers if len(bootstrap_servers) else [settings.BOOTSTRAP_SERVERS]
        self.admin_client = None

    async def get_admin_client(self) -> AIOKafkaAdminClient:
        if self.admin_client is None:
            self.admin_client = AIOKafkaAdminClient(
                bootstrap_servers=self.bootstrap_servers
            )
            await self.admin_client.start()
        return self.admin_client

    async def create_topic(self, topic_name: str, num_partitions: int = 1, replication_factor: int = 1) -> Dict[
        str, Any]:
        admin_client = await self.get_admin_client()

        topic_metadata = await admin_client.list_topics()
        if topic_name in topic_metadata:
            return {"status": HTTP_302_FOUND, "topic": topic_name}

        new_topic = NewTopic(
            name=topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )

        try:
            await admin_client.create_topics([new_topic])
            return {"status": HTTP_201_CREATED, "topic": topic_name}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create topic: {str(e)}")

    async def close(self):
        if self.admin_client is not None:
            await self.admin_client.close()
