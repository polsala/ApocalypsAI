resource "null_resource" "safehouse" {
  # The "triggers" map forces recreation when the message changes
  triggers = {
    welcome_message = var.welcome_message
  }

  provisioner "local-exec" {
    command = <<EOT
mkdir -p ${path.module}/safehouse &&
  echo "${var.welcome_message}" > ${path.module}/safehouse/message.txt
EOT
  }
}
