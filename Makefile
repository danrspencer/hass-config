IP=			hassio.local
USER=		root

update-config: update-secrets
	ssh ${USER}@${IP} "cd /config && git reset --hard origin/master && git pull && hassio homeassistant restart"

update-secrets:
	rsync -ae secrets.yaml ${USER}@${IP}:/config/secrets.yaml

logs:
	ssh ${USER}@${IP} "hassio homeassistant logs"

restart:
	ssh ${USER}@${IP} "hassio homeassistant restart"

secrets:
	cp ./config/secrets.yaml.sample ./config/secrets.yaml

get-config:
	rsync -ave ${USER}@${IP}:/config/* ./

get-backup:
	rsync -ave ${USER}@${IP}:/backup/* ./backup/

put-backup:
	rsync -ave ./backup/* ${USER}@${IP}:/backup/

reset-nest:
	ssh ${USER}@${IP} "sudo rm /home/homeassistant/.homeassistant/nest.con"
