#!/usr/bin/env bash
service rabbitmq-server restart
celery -A RetrievalEngine worker -B -l INFO -q
