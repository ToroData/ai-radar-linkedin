make deploy         # Launch infrastructure, update IP, and get Ansible ready
make ansible        # Run Ansible on the generated IP
make destroy        # Destroy the EC2 and clean up resources
make ping           # Verify SSH access with Ansible
