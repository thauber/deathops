# deathops

# install
Run bin/install.sh

# gcloud service account key for BQ access
gsutil cp gs://deathops-scratch/deathball-e3067788addd.json .  # or use console
cp deathball-e3067788addd.json /deathball/etc/db.json

# start supervisord, this runs the webapp
sudo systemctl start supervisord

# check it's running
Check /deathops/logs/webapp.log

# test streaming
$ curl -H 'Content-Type: application/json' -d '{"event": "test"}' 'http://localhost:8080/e'

# check the event logs:
$ cat /deathops/data/event.*.json

# take a look at bigquery
#standardsql
SELECT * FROM `deathball-180005.analytics.event`
order by ts desc
LIMIT 1000
