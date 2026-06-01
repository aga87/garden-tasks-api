ENV ?= prod

fmt:
	terraform fmt -recursive

validate:
	terraform validate

lint:
	tflint

plan: fmt validate lint
	terraform plan -var-file=$(ENV).tfvars

apply: fmt validate lint
	terraform apply -var-file=$(ENV).tfvars

destroy: fmt validate lint
	@read -p "Destroy $(ENV) resources? (yes/no): " confirm && [ "$$confirm" = "yes" ]
	terraform destroy -var-file=$(ENV).tfvars
