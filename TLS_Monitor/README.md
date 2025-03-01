# TLS Monitor
Python script to check for SSL/TLS certificate expiry.
## Usage
To run the check:
```
python3 monitor.py domains.yaml
```
Configuration file
```yaml
---
domain_groups:
  google_domains:
    domains:
      - 'www.google.com'
      - 'www.youtube.com'
    notification_groups:
      - google
    notify_before: 30
  amazon_domains:
    domains:
      - 'www.amazon.com'
      - 'www.primevideo.com'
    notification_groups:
      - amazon
    notify_before: 30

notification_groups:
  google:
    type: "mail"
    mail_meta:
      sender: "tls-monitor@google.com"
      receivers:
        - "ceo@google.com"
      subject: "Google TLS Certificate Expiry"
      username: "google"
      password: "G00GL3"
      server: "smtp.gmail.com"
  amazon:
    type: "mail"
    mail_meta:
      sender: "tls-monitor@amazon.com"
      receivers:
        - "ceo@amazon.com"
      subject: "Amazon TLS Certificate Expiry"
      username: "amazon"
      password: "Amaz0n"
      server: "smtp.amazon.com"
```
