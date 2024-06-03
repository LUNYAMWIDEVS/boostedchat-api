# Notes

## Check the number of Sent Tasks
```bash
docker compose logs api | grep "Sending due task SendFirstCompliment" | wc -l # assumes logs are only available for `today`
```

## Checking failed tasks




###
Create superuser

```python
manage.py createsuperuser
```

After migrating, run 

``` python
./manage.py loaddata channels channels.json
./manage.py loaddata channels channelActivities.json 
# Create salesReps manually # get sales_rep id and replace in fixture file
./manage.py loaddata channels salesRepChannels.json
./manage.py loaddata channels salesRepProfileList.json
./manage.py loaddata channels salesRepProfiles.json
```

## Issues
- [ ] ignoring existing data when `loaddata`
- [ ] fixtures in sales_rep not working. Quick fix: Moved them to channels


## Required Features
- [ ] add created_at, etc to all models.
- [ ] 