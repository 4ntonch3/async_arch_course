from faststream.kafka import KafkaBroker

import environment as env


broker = KafkaBroker(f"{env.BROKER_HOST}:{env.BROKER_PORT}")
