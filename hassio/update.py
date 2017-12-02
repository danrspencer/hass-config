#!/usr/bin/env python3

import requests
import yaml
import json

import os, re, sys

path = os.path.abspath(os.path.dirname(sys.argv[0]))

hass_url = sys.argv[1] if len(sys.argv) > 1 else 'http://hassio.local:8123'
secrets_path = sys.argv[2] if len(sys.argv) > 2 else '../secrets.yaml'

def main():
  secrets = load_yaml_file(path, secrets_path)

  update_repositories()
  update_installed()
  update_configs(secrets)

def update_repositories():
  addons_repositories = load_yaml_file(
    '%s/addons_repositories' % path, 
    'addons_repositories.yaml'
  )

  print('Updating Addons Repositories')
  post_to_api('supervisor/options', { 'addons_repositories': addons_repositories })

def update_installed():
  addons_installed = load_yaml_file(
    '%s/addons_repositories' % path, 
    'addons_installed.yaml'
  )

  for slug in addons_installed:
    print('Installing %s' % slug)
    post_to_api('addons/%s/install' % slug, {})

def update_configs(secrets):
  files = os.listdir('%s/addons' % path)
  regex = re.compile(r'(.*).yaml')

  for file in files:
    match = regex.search(file) 
    if not match:
      continue

    config = load_yaml_file('%s/addons' % path, file, secrets)

    slug = match.group(1)
    print('Updating config for %s' % slug)
    post_to_api('addons/%s/options' % slug, { 'options': config['options'] })
    post_to_api('addons/%s/restart' % slug, {})

def post_to_api(endpoint, body):
  url = '%s/api/hassio/%s' % (hass_url, endpoint)

  print('Request: %s' % url)
  print(body)

  response = requests.post(
    '%s/api/hassio/%s' % (hass_url, endpoint),
    json=body
  )

  print('Response: %s' % response.status_code)
  print(response.json())
  print('')
  
def load_yaml_file(path, filepath, secrets=[]):
  file = open('%s/%s' % (path, filepath), "r")
  content = file.readlines()
  file.close()
  
  enriched = enrich_with_secrets(content, secrets)

  return yaml.load('\n'.join(enriched))

def enrich_with_secrets(data, secrets): 
  regex = re.compile(r'(.*)(!secret (\w*))')

  enriched = []

  for line in data:
    match = regex.search(line)
    if not match: 
      enriched.append(line)
      continue

    secret_name = match.group(3)
    if not secret_name in secrets:
      raise ValueError('Could not find secret: "%s"' % secret_name)
      
    enriched.append('%s%s' % (match.group(1), secrets[secret_name]))
  
  return enriched

main()
