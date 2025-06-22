import json
import subprocess

output = subprocess.check_output(["terraform", "output", "-json"], cwd="terraform")
terraform_output = json.loads(output)

if "ec2_public_ip" not in terraform_output:
    raise KeyError("ec2_public_ip not found in Terraform output")

public_ip = terraform_output["ec2_public_ip"]["value"]

with open("ansible/hosts.ini", "w") as f:
    f.write(f"[ec2]\n{public_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/ai-linkedin.pem\n")

print(f"Updated Ansible inventory with EC2 public IP: {public_ip}")