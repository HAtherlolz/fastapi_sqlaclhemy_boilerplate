output "server_ipv4_address" {
  description = "Public IPv4 address of the server (use as GitHub secret HETZNER_HOST)"
  value       = hcloud_server.app.ipv4_address
}

output "server_id" {
  description = "Hetzner server ID"
  value       = hcloud_server.app.id
}

output "ssh_key_name" {
  description = "Name of the SSH key registered in Hetzner"
  value       = hcloud_ssh_key.deploy_key.name
}

output "ssh_command" {
  description = "Ready-to-use SSH command"
  value       = "ssh ${var.user}@${hcloud_server.app.ipv4_address}"
}
