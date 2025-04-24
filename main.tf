
provider "digitalocean" {
  token             = var.do_token
  spaces_access_id  = var.spaces_access_key_id
  spaces_secret_key = var.spaces_secret_key
}

resource "digitalocean_spaces_bucket" "media_bucket" {
  name   = var.spaces_bucket_name
  region = "nyc3"

  lifecycle {
    prevent_destroy = true
  }
  acl = "private"
}

resource "digitalocean_droplet" "plex_server" {
  image    = "ubuntu-22-04-x64"
  name     = "plex-server"
  region   = "nyc3"
  size     = "s-2vcpu-4gb"
  ssh_keys = [var.ssh_key_id]

  tags = ["PlexServer"]

  user_data = templatefile("${path.module}/user_data.yml", {
    spaces_access_key_id = var.spaces_access_key_id,
    spaces_secret_key    = var.spaces_secret_key,
    domain_name          = var.domain_name,
    email                = var.certbot_email,
    spaces_bucket_name   = var.spaces_bucket_name,
  })
}

resource "digitalocean_floating_ip" "web_ip" {
  region = digitalocean_droplet.plex_server.region
}

resource "digitalocean_floating_ip_assignment" "web_ip_assign" {
  ip_address = digitalocean_floating_ip.web_ip.ip_address
  droplet_id = digitalocean_droplet.plex_server.id
}

resource "digitalocean_firewall" "web" {
  name = "plex-firewall"

  droplet_ids = [digitalocean_droplet.plex_server.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "32400"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "80"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "443"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "53"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}