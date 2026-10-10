output "tree_names" {
  description = "List of generated tree identifiers"
  value       = [for i in range(var.tree_count) : random_pet.tree[i].id]
}
