import pika
import time
"""
client = mqtt.Client('devbox', clean_session=True)
client.username_pw_set('home', 'A@2cb13')
client.connect('192.168.43.200')
time.sleep(4)
client.publish("home/lab/benchlight", "toggle",pip )
"""
unpw = pika.PlainCredentials('home', 'A@2cb13')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.43.200', virtual_host='home', credentials=unpw)
)
channel = connection.channel()
channel.queue_declare(queue='lab/benchlight', durable=True)
channel.basic_publish(exchange='', body='toggle', routing_key='lab/benchlight')

print("message sent")