# webhook 2 mail gateway

Small script to receive a webhook and send a mail with that content.

# Quickstart

cp templates/example.mail templates/webhook.mail
vi templates/webhook.mail # edit template to taste (e.g. mail address)
python3 webhook.py

Then point your webhook to http://host/hook/mail

# Documentation

a json POST request to `/webhook/<path>` will use the template from `templates/webhook.<path>` to send an email.
