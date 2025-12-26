#!/bin/bash

cd "$(dirname "$0")"
set -ex

# Alapértelmezett config létrehozása
if [ ! -f .env ] ; then
  cp env.template .env
  echo "Default config created!"
fi

#Upgrade the database
if [ -f migrations/alembic.ini ] ; then
  /home/$USER/.local/bin/uv run flask db upgrade
fi

#Replace old cron job
currentpath=$(pwd)
username=$(whoami)
groupname=$(id -gn)
crontab -l | grep -v "LongWeekend" > newcron
echo "30 */6 * * * cd $currentpath && /home/$username/.local/bin/uv run flask scan >> $currentpath/log.log 2>&1" >> newcron
crontab newcron
rm newcron


servicename="LongWeekend-web"

if [ ! -f $servicename.service ] ; then
  cp $servicename.service.template $servicename.service
  sed -i "s|%currentpath%|$currentpath|g; s|%username%|$username|g; s|%groupname%|$groupname|g" $servicename.service
fi

if [ ! -f /etc/systemd/system/$servicename.service ] ; then
  sudo ln -s "$currentpath/$servicename.service" /etc/systemd/system/$servicename.service
fi

# Restart gunicorn
sudo systemctl daemon-reload
sudo systemctl enable $servicename
sudo systemctl restart $servicename