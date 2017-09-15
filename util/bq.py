import datetime
import itertools
import logging
import time
import traceback

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

log = logging.getLogger(__name__)


def get_service():
    svc, ts = getattr(ctx, 'google_bigquery_v2', (None, None))
    if not svc or (time.time() - ts > 30.0):
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/deathops/etc/bq.json')
        svc = build('bigquery', 'v2', credentials=credentials, cache_discovery=False)
        ctx.google_bigquery_v2 = (svc, time.time())
    return svc

def get_table(project_id, dataset_id, table_id):
    svc = get_service()
    try:
        res = svc.tables().get(projectId=project_id, datasetId=dataset_id, tableId=table_id).execute()
        return res
    except HttpError as e:
        if e.resp['status'] != '404':
            raise
    return None

def create_table(project_id, dataset_id, table_id, schema, **kwargs):
    body = {
        'kind': 'bigquery#table',
        'tableReference': {
            'projectId': project_id,
            'datasetId': dataset_id,
            'tableId': table_id,
        },
        'schema': {'fields': schema},
    }
    body.update(kwargs)
    svc = get_service()
    res = svc.tables().insert(projectId=project_id, datasetId=dataset_id, body=body).execute()
    return res

def ensure_dataset(project_id, dataset_id):
    svc = get_service()
    try:
        res = svc.datasets().get(projectId=project_id, datasetId=dataset_id).execute()
        return res
    except HttpError as e:
        if e.resp['status'] != '404':
            raise

    # create it
    res = svc.datasets().insert(projectId=project_id, body={'datasetReference': {'datasetId': dataset_id}}).execute()
    return res

def ensure_table(project_id, dataset_id, table_id, schema, **kwargs):
    ensure_dataset(project_id, dataset_id)

    svc = get_service()
    try:
        res = svc.tables().get(projectId=project_id, datasetId=dataset_id, tableId=table_id).execute()
        return res
    except HttpError as e:
        if e.resp['status'] != '404':
            raise

    return create_table(project_id, dataset_id, table_id, schema, **kwargs)

    svc = get_service()
    return svc.jobs().get(projectId=project_id, jobId=job_id).execute()

def insert_rows(project_id, dataset_id, table_id, rows, insert_id='id'):
    assert len(rows) <= 500, 'You can only insert 500 rows at a time...'

    res = None
    if not rows:
        return res

    svc = get_service()

    body = {'rows': [{'insertId': _[insert_id], 'json': _} for _ in rows]}
    for i in xrange(100):
        try:
            res = svc.tabledata().insertAll(projectId=project_id, datasetId=dataset_id,
                                            tableId=table_id, body=body).execute()
            assert not res.get('insertErrors'), res
            break
        except Exception:
            if i > 3:
                # tried 3 times, reraise
                raise
            print 'Exception inserting tabledata -- will retry:\n', traceback.format_exc()
            time.sleep(1)

    return res
