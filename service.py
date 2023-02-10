import logging
from os import urandom, environ
from typing import Tuple, Dict

from flask import Flask
from flask_apscheduler import APScheduler

from slot_machine import SlotMachine


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    logger.addHandler(logging.FileHandler('service.log', 'w+', 'utf-8'))
    return logger


def init_service(logger):
    app = Flask(
        'slot-engine'
    )
    app.config['SECRET_KEY'] = urandom(16)
    logger.warning('Secret key generated!')
    app.config['DEBUG'] = True if environ['DEBUG'] == 'true' else False
    try:
        instances = int(environ['INSTANCES'])
    except:
        instances = 1
    app.config['ENGINE_INSTANCES'] = tuple(
        [SlotMachine('config.json')] * instances
    )
    app.config['LOGGER'] = logger
    app.config['SCHEDULER_API_ENABLED'] = app.config['DEBUG']
    return app


app = init_service(init_logger())
scheduler = APScheduler()
scheduler.init_app(app)


@scheduler.task('cron', id='manage_workers', minute='*')
def manage_workers() -> None:
    """
    Regular check if current amount of workers is OK for current load.
    :return:
    """
    app.config['LOGGER'].debug('Regular task "manage_workers" executed.')


@app.route('/health', methods=['GET'])
def health() -> Tuple[Dict, int]:
    """
    Endpoint for reporting service is alive.
    :return:
    """
    return {
        'workers': len(app.config['ENGINE_INSTANCES'])
    }, 200


@app.route('/spin', methods=['GET'])
def spin(mode='normal', instance_num=None) -> Tuple[Dict, int]:
    """
    API endpoint for calling engine to make a spin.

    :param mode: spinning mode. Possible values can be:
        - normal
        - bonus
    :param instance_num: Instance number to perform spin. If None passed -
        spin will be made by first free instance.
    :return: Method returns tuple of:
        - dict of generated values
        - node assigned for client
        - status code
    """
    worker = SlotMachine.choose_available_instance(instance_num)
    if mode == 'normal':
        app.config['LOGGER'].debug('Rolled in NORMAL mode.')
        return {
            'roll': worker.roll(),
            'worker_id': worker.id
        }, 200
    elif mode == 'bonus':
        # not implemented
        app.config['LOGGER'].debug('Did not roll in BONUS mode.')
        return {'roll': {}, 'worker_id': worker.id}, 500
    else:
        app.config['LOGGER'].debug('Got bad roll mode.')
        return {'roll': {}, 'worker_id': 0}, 500


scheduler.start()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
