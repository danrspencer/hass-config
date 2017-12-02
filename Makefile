IP=			hassio.local
USER=		root

update-config: update-secrets
	ssh ${USER}@${IP} "cd /config && git reset --hard origin/master && git pull && hassio homeassistant restart"

update-secrets:
	scp -rp secrets.yaml ${USER}@${IP}:/config/secrets.yaml

update-hassio:
	hassio/

logs:
	ssh ${USER}@${IP} "hassio homeassistant logs"

restart:
	ssh ${USER}@${IP} "hassio homeassistant restart"

secrets:
	cp ./config/secrets.yaml.sample ./config/secrets.yaml

sync-config:
	scp -r ${USER}@${IP}:/config/*.yaml ./

get-backup:
	scp -rp ${USER}@${IP}:/backup/* ./backup/

put-backup:
	scp -rp ./backup/* ${USER}@${IP}:/backup/

reset-nest:
	ssh ${USER}@${IP} "sudo rm /home/homeassistant/.homeassistant/nest.con"
