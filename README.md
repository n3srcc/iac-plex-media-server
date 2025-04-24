# Plex Media Server Infrastructure with Terraform

This project uses Terraform to provision a complete Plex Media Server infrastructure on DigitalOcean, including:

- A Droplet running Ubuntu 22.04
- A DigitalOcean Spaces bucket for media storage
- Firewall rules to allow access to Plex
- Automatic SSL certificate via Certbot
- Optional floating IP for consistent public access
- Basic cloud-init setup for Plex installation and Nginx reverse proxy

## Prerequisites

- [Terraform](https://www.terraform.io/downloads)
- A [DigitalOcean](https://www.digitalocean.com/) account
- A registered domain pointing to DigitalOcean's DNS
- SSH key added to your DigitalOcean account
- `rclone` (used in the instance to mount Spaces bucket)
- A DNS A record pointing to your floating IP

## Usage

### 1. **Configure the environment**

Create a file named `terraform.tfvars` and replace the values with your actual credentials and settings:

```hcl
do_token              = "your_digitalocean_token"
ssh_key_id            = "your_ssh_key_id"
spaces_access_key_id  = "your_spaces_access_key"
spaces_secret_key     = "your_spaces_secret"
spaces_bucket_name    = "your_bucket_name"
domain_name           = "media.yourdomain.com"
certbot_email         = "you@example.com"
