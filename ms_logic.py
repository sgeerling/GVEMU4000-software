# -*- coding: utf-8 -*-

#https://www.python.org/dev/peps/pep-0008/

import logging
import os
import database.db_services as _db_service
import traceback
import time
import json
from utils.utils import MissingConfigurationError, SqlInsertingError, DuplicateKeyError
from models.queue import Queue
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pika.exceptions import ConnectionClosed
from database.db import Database
from datetime import datetime as dt

logging.basicConfig(level=int(os.environ['DEFAULT_LOGGING_LEVEL']),
                    format='%(asctime)s %(process)s %(levelname)-8s %(name)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)
logger = logging.getLogger(__name__)


def queue_execution(params):
    """
    :params: dictionary with configurations params to be used in the function
    :return:
    """
    # First we take note of the time at what this process began. time.time() returns a non timezone date
    start_time = time.time()

    # Create the rabbitmq and sqlengine infrastructure to properly consume the queue
    db = Database()

    consumption_queue = Queue(params['can_event_amqp_url'], params['can_event_queue_name'])
    consumption_queue.connect()
    consumption_queue.create_channel()

    trigger_sleep_time = True

    # Start a loop that consumes and process one message at a time. We use a simple iterator for that
    # gopimn: change to 1 just for testing
    message_limit = 1 #params['message_limit']
    for i in range(message_limit):
        try:
            # Initialize message as none to make control flow with it.
            can_event_message = None
            print(str("inserting dummy"))
            #can_alert_id = _db_service.save_queue_raw(db, "Dummy")
            # print(str(can_alert_id))
            # Get input queue message
            can_event_message, method_frame, header_frame, body = consumption_queue.get_message_from_channel(consumption_queue.channel)

            if can_event_message:
                print(str(can_event_message))
                
                # Save alert in data base
                can_alert_id = _db_service.save_queue_raw(db, can_event_message)
                print(str(can_alert_id))
                print(str("Sending ACK"))
                consumption_queue.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                logger.log(21, "SUCCESS processing alerts for can event message id: +"+str(can_alert_id))
                continue
                
            elif can_event_message is None:
                continue
            
            else:
                logger.log(21, "No Harsh Braking Alert for can_event_instant_record_two {0}.".format(source_table_record_id))
                continue
            # Database saving and alert enqueuing was successful: acknowledge the queue.

        except SQLAlchemyError as e:
            print(traceback.format_exc())
            logger.error(e)
            # As we don't know the nature of this exception, reject and re publish message
            consumption_queue.channel.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)
            encoded_message = json.dumps(can_event_message, separators=(',', ':'))
            consumption_queue.channel.basic_publish(exchange=method_frame.exchange, routing_key=method_frame.routing_key,
                                                    body=encoded_message, properties=header_frame, mandatory=True)
            # Log the case
            logger.log(40, "Error, requeue=False but republished in message id: +" + str(source_table_record_id) +"+ in table name +" + str(source_table_name))
            logger.log(40, str(traceback.format_exc()))
            continue
        
        except IntegrityError as e:
            print(traceback.format_exc())
            logger.error(e)
            # In this case, there is a problem with the sql we are generating, reject message with requeue false
            consumption_queue.channel.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)
            # Log the case
            logger.log(40, "Error, requeue=True in message id: +" + str(source_table_record_id) +"+ in table name +" + str(source_table_name))
            logger.log(40, str(traceback.format_exc()))
            continue
        
        except MissingConfigurationError as e:
            
            print(traceback.format_exc())
            logger.error(e)
            
            # As we don't know the nature of this exception, reject and re publish message
            consumption_queue.channel.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)
            encoded_message = json.dumps(can_event_message, separators=(',', ':'))
            consumption_queue.channel.basic_publish(exchange=method_frame.exchange, routing_key=method_frame.routing_key, body=encoded_message, properties=header_frame, mandatory=True)
            
            # Log the case
            logger.log(40, "Error, requeue=False but republished in message id: +" + str(source_table_record_id) +"+ in table name +" + str(source_table_name))
            logger.log(40, str(traceback.format_exc()))
            continue
        
        except SqlInsertingError as e:
            print(traceback.format_exc())
            logger.error(e)
            # As we don't know the nature of this exception, reject and re publish message
            consumption_queue.channel.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)
            encoded_message = json.dumps(can_event_message, separators=(',', ':'))
            consumption_queue.channel.basic_publish(exchange=method_frame.exchange, routing_key=method_frame.routing_key, body=encoded_message, properties=header_frame, mandatory=True)
            # Log the case
            logger.log(40, "Error, requeue=False but republished in message id: +" + str(source_table_record_id) +"+ in table name +" + str(source_table_name))
            logger.log(40, str(traceback.format_exc()))
            continue
        
        except DuplicateKeyError as e:
            print(traceback.format_exc())
            logger.error(e)
            consumption_queue.channel.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)
            logger.log(40, "Error, requeue=False in  message id: +" + str(source_table_record_id) +"+ in table name +" + str(source_table_name))
            logger.log(40, str(traceback.format_exc()))
            continue
        
        except ConnectionClosed as e:
            print(traceback.format_exc())
            logger.error(e)
            logger.log(40, "Error, connection closed in message id: +" + str(source_table_record_id) +"+ in table name +" + str(source_table_name))
            logger.log(40, str(traceback.format_exc()))
            continue
        
        except AttributeError as e:
            # And check if the queue is empty
            if can_event_message is None:
                print("Queue is already empty. Going to sleep...")
                break
            else:
                print(traceback.format_exc())
                logger.error(e)
                print("Error de atributo. Posiblemente algún problema con los datos en este mensaje. "
                      "Se procede a rechazar")
                consumption_queue.channel.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)
            continue
        
        except Exception as e:
            print(traceback.format_exc())
            logger.error(e)
            # As we don't know the nature of this exception, a conservative approach will be excecuted:
            # The message will be rejected without requeing, and the information will be inserted in the queue as
            # a new message at the back of it.
            consumption_queue.channel.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)
            encoded_message = json.dumps(can_event_message, separators=(',', ':'))
            consumption_queue.channel.basic_publish(exchange=method_frame.exchange, routing_key=method_frame.routing_key,
                                                    body=encoded_message, properties=header_frame, mandatory=True)
            # Log the case
            logger.log(40, "Error, requeue=False but republished in message id: +" + str(source_table_record_id) +"+ in table name +" + str(source_table_name))
            logger.log(40, str(traceback.format_exc()))
            continue

    consumption_queue.close_connection()  # Close connection
    end_time = time.time()  # As with starting time, we take note of the ending time, and return duration of the process
    process_time = end_time - start_time
    logger.info('Duration: ' + str(end_time - start_time) + "\n")
    return process_time, trigger_sleep_time
