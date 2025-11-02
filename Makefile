.PHONY: build

deploy-infra: sam build && aws-vault exec Julie-Leon --no-session sam deploy

deploy-site: aws-vault exec Julie-Leon --no-session -- aws s3 sync ./resume-content s3://my-cloud-portfolio-website --region us-east-1