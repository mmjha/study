# https://faust.readthedocs.io/en/latest/playbooks/leaderelection.html#starting-kafka
# faust -A leader worker -l info --web-port 6066
# faust -A leader worker -l info --web-port 6067
# faust -A leader worker -l info --web-port 6068

import faust

app = faust.App(
    'leader-example',
    broker='kafka://localhost:9092',
    value_serializer='raw',
)

@app.agent()
async def say(greetings):
    async for greeting in greetings:
        print(greeting)

import random

@app.timer(2.0, on_leader=True)
async def publish_greetings():
    print('PUBLISHING ON LEADER!')
    greeting = str(random.random())
    await say.send(value=greeting)
