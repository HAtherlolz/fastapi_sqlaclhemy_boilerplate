#cloud-config
users:
  - name: ${deploy_user}
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    ssh_authorized_keys:
      - ${ssh_public_key}

runcmd:
  - apt-get update -y
  - apt-get upgrade -y
  - apt-get install -y ca-certificates curl gnupg lsb-release git rsync
  - mkdir -p /etc/apt/keyrings
  - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  - chmod a+r /etc/apt/keyrings/docker.gpg
  - echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
  - apt-get update -y
  - apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  - systemctl enable --now docker
  - mkdir -p /home/${deploy_user}/app
  - chown -R ${deploy_user}:${deploy_user} /home/${deploy_user}/app
  - usermod -aG docker ${deploy_user} || true
  - echo "Provisioned by Terraform (Hetzner)" > /tmp/hetzner-provisioned
