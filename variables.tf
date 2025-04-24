variable "do_token" {
  description = "Token de API de DigitalOcean"
  type        = string
}

variable "ssh_key_id" {
  description = "ID de la clave SSH en DigitalOcean"
  type        = string
}

variable "spaces_access_key_id" {
  description = "Access Key Id para el bucket de Spaces"
  type        = string
  sensitive   = true
}

variable "spaces_secret_key" {
  description = "Secret Key para el bucket de Spaces"
  type        = string
  sensitive   = true
}

variable "spaces_bucket_name" {
  description = "Nombre del bucket de Spaces"
  type        = string
}

variable "domain_name" {
  description = "Nombre de dominio para el servidor Plex"
  type        = string
}

variable "certbot_email" {
  description = "Email para Certbot"
  type        = string
  default     = null
}
