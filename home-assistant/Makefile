IP=			192.168.0.35
USER=		pi
PASS=		raspberry

get-config:
	echo raspberry | pbcopy
	scp ${USER}@${IP}:/home/homeassistant/.homeassistant/*.yaml ./config

put-config:
	echo raspberry | pbcopy
	scp ./config/*.yaml ${USER}@${IP}:/home/homeassistant/.homeassistant
