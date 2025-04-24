output "droplet_ip" {
  description = "Dirección IP del Droplet de Plex"
  value       = digitalocean_droplet.plex_server.ipv4_address
}

output "spaces_endpoint" {
  description = "Endpoint del bucket de Spaces"
  value       = digitalocean_spaces_bucket.media_bucket.endpoint
}
