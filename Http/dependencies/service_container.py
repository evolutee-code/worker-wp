from dependency_injector import containers, providers
from mona_package.services.kafka.kafka_admin_service import KafkaAdminService
from mona_package.services.kafka.kafka_producer_service import KafkaProducerService

from Http.services.kafka_service import KafkaService
from Http.services.validate_upload_service import ValidateUploadService


class ServiceContainer(containers.DeclarativeContainer):
    upload_service = providers.Factory(
        ValidateUploadService,
    )

    kafka_admin_service = providers.Singleton(KafkaAdminService)
    kafka_producer_service = providers.Singleton(KafkaProducerService)

    kafka_service = providers.Factory(
        KafkaService,
        kafka_admin_service=kafka_admin_service,
        kafka_producer_service=kafka_producer_service,
    )
