import random
import time
from paho.mqtt import client as mqtt_client


BROKER_HOST = '127.0.0.0' # IP/Hostname of the MQTT broker
BROKER_PORT = 1883 # Port of the MQTT broker
TOPIC = 'topic/group/identifier' # MQTT topic to publish to
client_id = f'my-device-mqtt-{random.randint(0,1000)}' # Unique client ID for the MQTT client

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def connect_mqtt():
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			print("Connected to MQTT Broker!")
		else:
			print("Failed to connect, return code: %d\n", rc)
			
	def on_disconnect(client, userdata, rc):
		print("Disconnected with result code: %s", rc)
		reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
		
        # Auto reconnect logic
		while reconnect_count < MAX_RECONNECT_COUNT:
			print("Reconnecting in %d seconds...", reconnect_delay)
			time.sleep(reconnect_delay)
			
			try:
				client.reconnect()
				print("Reconnected successfully!")
				return
			except Exception as err:
				print("%s. Reconnect failed. Retrying...", err)
				
			reconnect_delay *= RECONNECT_RATE
			reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
			reconnect_count += 1
		print("Reconnect failed after %s attempts. Exiting...", reconnect_count)
			
	client = mqtt_client.Client(client_id)
	
	#client.username_pw_set(username, password) # Uncomment if authentication is needed
	client.on_connect = on_connect
	client.on_disconnect = on_disconnect
	
	#client.connect(BROKER_HOST, BROKER_PORT) # Uncomment to connect synchronously
	client.connect_async(BROKER_HOST, port=BROKER_PORT, keepalive=60)
	return client
	
def publish(client):
	while True:
		time.sleep(5)
		data = None  # Replace with actual data reading logic
		result = client.publish(TOPIC, data)
		status = result[0]
		
		if not status == 0:
			print(f"Failed to send data to topic `{TOPIC}`")

			
def run():
	client = connect_mqtt()
	client.loop_start()
	publish(client)
	client.loop_stop()
	
if __name__ == '__main__':
	run()
