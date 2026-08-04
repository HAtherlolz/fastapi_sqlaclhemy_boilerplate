resource "hcloud_ssh_key" "deploy_key" {
  name       = var.ssh_key_name
  public_key = var.ssh_public_key
}

resource "hcloud_server" "app" {
  name        = var.server_name
  server_type = var.server_type
  image       = var.image
  location    = var.location != "" ? var.location : null
  ssh_keys    = [hcloud_ssh_key.deploy_key.name]
  user_data = templatefile("${path.module}/cloud-init.tpl", {
    ssh_public_key = var.ssh_public_key,
    deploy_user    = var.user
  })

  labels = {
    app = var.server_name
  }
}

resource "hcloud_firewall" "fw" {
  count = var.create_firewall ? 1 : 0
  name  = "${var.server_name}-fw"

  dynamic "rule" {
    for_each = var.allowed_ports
    content {
      direction  = "in"
      protocol   = "tcp"
      port       = tostring(rule.value)
      source_ips = ["0.0.0.0/0", "::/0"]
    }
  }
}

resource "hcloud_firewall_attachment" "fw_attach" {
  count       = var.create_firewall ? 1 : 0
  firewall_id = hcloud_firewall.fw[0].id
  server_ids  = [hcloud_server.app.id]
}
