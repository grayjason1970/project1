import boto3
import time
import paramiko
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Initialize Boto3 clients
ec2 = boto3.resource('ec2', region_name='us-west-2')
client = boto3.client('ec2', region_name='us-west-2')

# Variables (update values)
ami_id = 'ami-0648742c7600c103f'  # Amazon Linux 2 AMI
instance_type = 't2.micro'
key_name = 'your-key-pair'  # Replace key pair name
security_group_id = 'your-security-group-id'  # Replace security group ID
subnet_id = 'your-subnet-id'  # Replace servers subnet ID
region = 'us-west-2'
db_password = 'your-db-password'  # Replace MySQL root password

# Function to create an EC2 instance
def create_instance():
    try:
        instances = ec2.create_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName=key_name,
            NetworkInterfaces=[{
                'SubnetId': subnet_id,
                'DeviceIndex': 0,
                'AssociatePublicIpAddress': True,
                'Groups': [security_group_id]
            }],
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'mysql-server'}]
            }]
        )

        instance_id = instances[0].id
        print(f'Created instance with ID: {instance_id}')
        return instance_id
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(e)
        return None

# Function to wait until the instance status is OK
def wait_for_instance(instance_id):
    waiter = client.get_waiter('instance_status_ok')
    waiter.wait(InstanceIds=[instance_id])
    print(f'Instance {instance_id} is in running state and passed status checks')

# Function to install MySQL and initialize the database
def setup_mysql(instance_id):
    instance = ec2.Instance(instance_id)
    public_ip = instance.public_ip_address

    key = paramiko.RSAKey(filename=f'/Users/jasongray/{key_name}.pem')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Wait for the instance to be ready for SSH
    time.sleep(60)

    ssh.connect(public_ip, username='ec2-user', pkey=key)

    commands = [
        'sudo yum update -y',
        'sudo amazon-linux-extras install epel -y',
        'sudo yum update -y',
        'sudo amazon-linux-extras install mariadb10.5 -y',
        'sudo systemctl start mariadb',
        'sudo systemctl enable mariadb',
    ]

    # Execute commands
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())

    # MySQL secure installation commands
    mysql_commands = f"""
    sudo  /usr/bin/mysqladmin -u root password '{db_password}',
    sudo mysql -u root -p'{db_password}' -e "CREATE DATABASE project1;",
    sudo mysql -e \"USE project1; CREATE TABLE images (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255));\",
    sudo mysql -e \"USE project1; CREATE TABLE instance_types (id INT PRIMARY KEY AUTO_INCREMENT, type VARCHAR(255));\",
    sudo mysql -e \"USE project1; CREATE TABLE instances (id INT PRIMARY KEY AUTO_INCREMENT, instance_id VARCHAR(255));\",
    sudo mysql -e \"USE project1; CREATE TABLE memory_sizes (id INT PRIMARY KEY AUTO_INCREMENT, size VARCHAR(255));\",
    sudo mysql -e \"USE project1; CREATE TABLE disk_sizes (id INT PRIMARY KEY AUTO_INCREMENT, size VARCHAR(255));\",
    sudo mysql -e \"USE project1; CREATE TABLE subnet_id (id INT PRIMARY KEY AUTO_INCREMENT, zone VARCHAR(255));\"
    sudo mysql -e \"USE project1; CREATE TABLE key_pairs (id INT AUTO_INCREMENT PRIMARY KEY, key_name VARCHAR(255) NOT NULL, private_key TEXT NOT NULL);\",
    sudo mysql -e \"USE project1; INSERT INTO images (name) VALUES ('ami-12345678'), ('ami-87654321');\",
    sudo mysql -e \"USE project1; INSERT INTO instance_types (type) VALUES ('t2.micro'), ('t2.small'), ('t2.medium');\",
    sudo mysql -e \"USE project1; INSERT INTO memory_sizes (size) VALUES ('1GB'), ('2GB'), ('4GB');\",
    sudo mysql -e \"USE project1; INSERT INTO disk_sizes (size) VALUES ('8GB'), ('16GB'), ('32GB');\",
    sudo mysql -e \"USE project1; INSERT INTO subnet_id (subnet) VALUES ('subnet-03d934629af7d951e'), ('subnet-0765bf5ae4bb935f7');\"
    """
    
    ssh.close()
    print(f'MySQL setup on instance {instance_id} with public IP {public_ip}')

# Main execution
instance_id = create_instance()
if instance_id:
    wait_for_instance(instance_id)
    setup_mysql(instance_id)
