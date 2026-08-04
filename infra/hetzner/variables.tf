variable "hcloud_token" {
  type        = string
  description = "Hetzner Cloud API token"
  sensitive   = true
}

variable "ssh_public_key" {
  type        = string
  description = "SSH public key to add to the server (one-line, e.g. ssh-ed25519 ...)"
}

variable "ssh_key_name" {
  type        = string
  description = "Name for SSH key in Hetzner"
  default     = "autopro-deploy-key"
}

variable "server_name" {
  type        = string
  description = "Name of the Hetzner server"
  default     = "autopro"
}

variable "server_type" {
  type        = string
  default     = "cpx22" # 2 vCPU, 4 GB RAM (AMD, x86) — доступен в nbg1/hel1/sin
  description = "Hetzner server type. cpx22 = 2 vCPU/4GB; cpx32 = 4 vCPU/8GB. Проверить доступность в локации можно в Hetzner Console."
}

variable "image" {
  type        = string
  description = "OS image for the server"
  default     = "ubuntu-24.04"
}

variable "location" {
  type = string
  # cpx22 доступен в nbg1 (Nuremberg), hel1 (Helsinki), sin (Singapore).
  # Набор типов зависит от локации — свериться можно через API /datacenters.
  default     = "nbg1"
  description = "Hetzner location. Для server_type=cpx22 подходят nbg1 / hel1 / sin"
}

variable "user" {
  type        = string
  default     = "deploy"
  description = "User to create on the server for deployments"
}

variable "create_firewall" {
  type        = bool
  description = "Whether to create and attach a Hetzner firewall"
  default     = true
}

variable "allowed_ports" {
  type        = list(number)
  description = "Inbound TCP ports opened by the firewall"
  default     = [22, 80, 443]
}
