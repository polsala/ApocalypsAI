resource "template_file" "cloud_init_user_data" {
  template = file("${path.module}/templates/cloud_init.yaml.tpl")

  vars = {
    instance_name    = var.instance_name
    banner_message   = var.banner_message
    user_data_script = var.user_data_script
    package_list     = var.package_list
  }
}

variable "instance_name" {
  description = "A name for the instance, used in the whimsical banner."
  type        = string
  default     = "ApocalypsAI Instance"
}

variable "banner_message" {
  description = "The core message for the whimsical banner."
  type        = string
  default     = "Greetings from the digital ether!"
}

variable "user_data_script" {
  description = "A string containing a shell script to be executed by cloud-init."
  type        = string
  default     = null
}

variable "package_list" {
  description = "A list of packages to install via `apt-get`."
  type        = list(string)
  default     = []
}

output "user_data" {
  description = "The generated `cloud-init` user data string."
  value       = template_file.cloud_init_user_data.rendered
}
