import tweepy
import conf, json, time
from boltiot import Bolt

config = {
	"consumer_key" : conf.consumer_key,
	"consumer_secret" : conf.consumer_secret,
	"access_token" : conf.access_token,
	"access_token_secret" : conf.access_token_secret
}

def get_api_object(cfg):
	auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
	auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
	return tweepy.API(auth)


mybolt = Bolt(conf.bolt_cloud_api_key, conf.device_id)
temperature_threshold = 59


while True:
	response = mybolt.analogRead('A0')
	data = json.loads(response)
	print (data['value'])
	try:
		sensor_value = int(data['value'])
		if sensor_value > temperature_threshold:
			print ("Temperature has crossed the threshold.")
			api_object = get_api_object(config)
			tweet = ("Temperature has crossed the threshold")
			status = api_object.update_status(status=tweet)
	except Exception as e:
		print("An error occured", e)
	time.sleep(10)



