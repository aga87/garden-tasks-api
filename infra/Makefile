fmt:
	terraform fmt -recursive

validate:
	terraform validate

lint:
	tflint
	
plan-prod: fmt validate lint
	terraform plan -var-file=prod.tfvars

apply-prod: fmt validate lint
	terraform apply -var-file=prod.tfvars

destroy-prod: fmt validate lint
	@read -p "Destroy PROD resources? (yes/no): " confirm && [ "$$confirm" = "yes" ]
	terraform destroy -var-file=prod.tfvars