provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where the EC2 instance will be launched"
  type        = string
}

# Ubuntu 24.04 LTS, x86_64
data "aws_ami" "ubuntu_2404" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "image-id"
    values = ["ami-04ec97dc75ac850b1"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

data "aws_subnets" "default_subnets" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
}

data "aws_subnet" "selected" {
  id = data.aws_subnets.default_subnets.ids[0]
}

resource "aws_instance" "ai_radar_instance" {
  ami                    = data.aws_ami.ubuntu_2404.id
  instance_type          = "t2.medium"
  key_name               = "ai-linkedin"
  subnet_id              = data.aws_subnet.selected.id
  vpc_security_group_ids = ["sg-08ca8caa7b5695913"]

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
  }

  tags = {
    Name = "ai-radar-instance"
  }
}

output "ec2_public_ip" {
  value = aws_instance.ai_radar_instance.public_ip
}
