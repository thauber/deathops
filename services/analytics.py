import datetime
import json
import logging
import os
import time
import util.bq
import uuid

log = logging.getLogger(__name__)

project_id = 'deathball-180005'
dataset_id = 'analytics'
table_id = 'event'

schema = [
    {'name': 'event', 'type': 'string'},
    {'name': 'ts', 'type': 'timestamp'},
    {'name': 'id', 'type': 'string'},
    {'name': 'app_id', 'type': 'string', 'mode': 'nullable'},
    {'name': 'system_id', 'type': 'string', 'mode': 'nullable'},
    {'name': 'context', 'type': 'string', 'mode': 'nullable'},
]

util.bq.ensure_table(project_id, dataset_id, table_id, schema)

fout = open('/deathops/data/event.%s.%s.json' % (datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'), os.getpid()), 'a')

def insert_events(evts):
    for evt in evts:
        evt['ts'] = datetime.datetime.utcnow().isoformat()[:-3] + 'Z'
        evt['id'] = str(uuid.uuid1())
        fout.write(json.dumps(evt) + '\n')
        fout.flush()

    for i in xrange(10):
        try:
            util.bq.insert_rows(project_id, dataset_id, table_id, evts)
            break
        except Exception:
            time.sleep(2)
            if i > 5:
                raise
