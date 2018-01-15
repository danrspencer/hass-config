#!/usr/bin/env python3

import requests
import yaml
import json

import os, sys

path = os.path.abspath(os.path.dirname(sys.argv[0])) 

hass_url = sys.argv[1] if len(sys.argv) > 1 else "http://hassio.local:8123"

def main():
  response = requests.get('%s/api/hassio/supervisor/info' % hass_url)

  supervisor_info = response.json()['data']
  installed = backup_addons(supervisor_info)

  write_file(
    "%s/addons_repositories"  % path,
    "addons_repositories.yaml",
    supervisor_info['addons_repositories']
  )
  
  write_file(
    "%s/addons_repositories"  % path,
    "addons_installed.yaml",
    installed
  )

def backup_addons(supervisor_info):
  installed = []

  for addon_info in supervisor_info['addons']:
    slug = addon_info['slug']
    installed.append(slug)

    addon_data = get_addon_details(slug)

    write_file(
      "%s/addons" % path,
      "%s.yaml" % slug.lower(),
      addon_data
    )

  return installed

def get_addon_details(slug):
  response = requests.get('%s/api/hassio/addons/%s/info' % (hass_url, slug))

  data = response.json()['data']
  addon = { key: data[key] for key in ['name', 'url', 'options'] }

  return addon

def write_file(path, filename, contents):
  try:
    os.mkdir(path)
  except Exception:
    pass

  file = open("%s/%s" % (path, filename), "w")
  file.write(yaml.dump(contents, default_flow_style=False))
  file.close()

main()
