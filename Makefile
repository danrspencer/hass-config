REMOTE=root@hassio.local

update-config: update-secrets
	ssh ${REMOTE} "cd /config && git reset --hard origin/master && git pull origin master && hassio homeassistant restart"

update-secrets:
	scp -rp ./secrets.yaml ${REMOTE}:/config/secrets.yaml

update-hassio:
	hassio/update.py

logs:
	ssh ${REMOTE} "hassio homeassistant logs"

restart:
	ssh ${REMOTE} "hassio homeassistant restart"

secrets:
	cp ./secrets.yaml.sample ./config/secrets.yaml

sync-config:
	scp -r ${REMOTE}:/config/*.yaml ./

get-backup:
	scp -rp ${REMOTE}:/backup/* ./backup/

put-backup:
	scp -rp ./backup/* ${REMOTE}:/backup/

setup-config-git:
	ssh ${REMOTE} "cd /config && " \
		"git init &&" \
		"git remote add origin -f https://github.com/danrspencer/hass-config.git &&" \
		"git pull origin master"

reset-nest:
	ssh ${REMOTE} "sudo rm /home/homeassistant/.homeassistant/nest.con"

update-to-version:
	ssh ${REMOTE} "curl -d '{\"version\": \"${VERSION}\"}' http://hassio/homeassistant/update"
