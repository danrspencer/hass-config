IP=			***REMOVED***.duckdns.org
USER=		root

update-config:
	ssh ${USER}@${IP} "cd /config && git pull"

update-secrets:
	scp -rp secrets.yaml ${USER}@${IP}:/config/secrets.yaml

logs:
	ssh ${USER}@${IP} "hassio homeassistant logs"

restart:
	ssh ${USER}@${IP} "hassio homeassistant restart"

get-config:
	scp -rp ${USER}@${IP}:/config/{*.yaml,**/*.yaml,*.conf} ./config

secrets:
	cp ./config/secrets.yaml.sample ./config/secrets.yaml

reset-nest:
	ssh ${USER}@${IP} "sudo rm /home/homeassistant/.homeassistant/nest.con"
