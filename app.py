# -*- coding: utf-8 -*-
"""
@author: gopimn
"""
import os
import time
import logging
import traceback
import ms_logic as ms_logic

# Just for the test, create the environment variables:
os.system('source ./environment/opentracker_local.sh')

print(int(os.environ['DEFAULT_LOGGING_LEVEL']))

logging.basicConfig(level=int(os.environ['DEFAULT_LOGGING_LEVEL']), format='%(asctime)s %(process)s %(levelname)-8s %(name)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',)
logger = logging.getLogger(__name__)


# 
base_sleep_time = 0.06#int(os.environ['MS_BASE_SLEEP_TIME_MINUTES'])

params = {}
params['message_limit'] = int(os.environ['MESSAGE_LIMIT'])
params['can_event_amqp_url'] = os.environ['CAN_EVENTS_AMQP_CONN']
params['can_event_queue_name'] = os.environ['CAN_TEST_QUEUE']

while True:
	try:
		start_time = time.time()
		print("Starting process at " + time.strftime("%b %d %Y %H:%M:%S", time.gmtime(time.time())) + " UTC time.")
		process_time, trigger_sleep_time = ms_logic.queue_execution(params)
		process_time_minutes = process_time * 0.01666666 # 1/60
		print("The last processing took " + str(process_time_minutes) + " minutes in its execution.")

		try:
			still_alive = send_still_alive_notification()
		except Exception as e:
			logger.warning("Unable to send keep alive {0}".format(e))

	except Exception as e:
		print(traceback.format_exc())
		end_time = time.time()
		process_time_minutes = (end_time - start_time) / 60.0
		logger.critical("Process iteration going down...!")
		logger.critical("{0}".format(e))
                
	finally:
		#sleep_time = max(base_sleep_time - process_time_minutes, 0)
		#print("The service will sleep " + str(sleep_time) + " minutes.")
		#logging.info("Sleeping {0} seconds".format(sleep_time))
		#time.sleep(sleep_time * 60.0)
		logging.info("New cycle of 0 minutes for other processing...")#.format(sleep_time))
                        
