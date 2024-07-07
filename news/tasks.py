#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import shared_task
from news.management.commands import runapscheduler
import time


@shared_task
def hello():
    time.sleep(3)
    return "Hello, world!"


@shared_task
def printer(n):
    for i in range(n):
        time.sleep(1)
        print(i + 1)


@shared_task()
def send_news():
    runapscheduler.Command()

