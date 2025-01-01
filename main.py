import boto3

ec2 = boto3.client('ec2')

def create_network():
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id=vpc['Vpc']["VpcId"]
    print("vpc successfully created\n VPC ID :"+ vpc_id)
    ec2.create_tags(Resources=[vpc_id], Tags=[{"Key": "Name", "Value": "VPCSDK"}])


    public_subnet= ec2.create_subnet(VpcId=vpc_id, CidrBlock= '10.0.1.0/24')
    public_subnet_id= public_subnet['Subnet']['SubnetId']
    print("public subnet successfully created \npublic subnet ID :"+ public_subnet_id)
    ec2.create_tags(Resources=[public_subnet_id], Tags=[{"Key": "Name", "Value": "PublicSubnetSDK"}])

    private_subnet = ec2.create_subnet(VpcId=vpc_id, CidrBlock= '10.0.2.0/24')
    private_subnet_id= private_subnet['Subnet']['SubnetId']
    print("private subnet successfully created \nprivate subnet ID :"+ private_subnet_id)
    ec2.create_tags(Resources=[private_subnet_id], Tags=[{"Key": "Name", "Value": "PrivateSubnetSDK"}])

    InternetGateway = ec2.create_internet_gateway()
    InternetGateway_id = InternetGateway['InternetGateway']['InternetGatewayId']
    print("internet gateway sucessfully created \ninternetgateway ID : " + InternetGateway_id)
    ec2.create_tags(Resources=[InternetGateway_id], Tags=[{"Key": "Name", "Value": "InternetGatewaySDK"}])

    ec2.attach_internet_gateway(InternetGatewayId=InternetGateway_id, VpcId=vpc_id)

    return vpc_id, public_subnet_id, private_subnet_id, InternetGateway_id

def destroy(vpc_id, public_subnet_id, private_subnet_id, InternetGateway_id):
    ec2.detach_internet_gateway(InternetGatewayId=InternetGateway_id, VpcId=vpc_id)
    ec2.delete_internet_gateway(InternetGatewayId=InternetGateway_id)
    print("internet gateway deatached and deleted")
    ec2.delete_subnet(SubnetId=public_subnet_id)
    ec2.delete_subnet(SubnetId=private_subnet_id)
    print("subnets are deleted")
    ec2.delete_vpc(VpcId=vpc_id)
    print("vpc is deleted")

if __name__ == "__main__":
    vpc_id, public_subnet_id, private_subnet_id, InternetGateway_id = create_network()
    ##destroy(vpc_id, public_subnet_id, private_subnet_id, InternetGateway_id)