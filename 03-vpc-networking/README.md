🚀 AWS Cloud Learning Journey — Lab 03: VPC & Networking Fundamentals

This lab took me deeper into how AWS networking actually works.

Instead of using the default AWS network, I built a custom VPC from scratch and connected the different components needed for an EC2 instance to communicate with the internet.

I worked with:

• Amazon VPC
• CIDR blocks
• Subnets
• Internet Gateways
• Route Tables
• Security Groups
• Amazon EC2
• SSH and Linux networking commands

I created a `10.0.0.0/16` VPC, added a `10.0.1.0/24` subnet, configured an Internet Gateway and route table, and then launched an EC2 instance inside the custom network.

I also connected to the instance through SSH and used commands such as `ip addr`, `ip route`, and `curl` to verify the network configuration and internet connectivity.

One of my biggest takeaways from this lab was understanding that a subnet isn't simply "public" because we name it public. The routing configuration, Internet Gateway, public IP, and security rules all have a role in making connectivity possible.

I'm documenting each lab as I continue building practical AWS and cloud infrastructure skills.

🔗 GitHub: https://github.com/Austine192-A/aws-cloud-journey

Next: Amazon RDS PostgreSQL ☁️

#AWS #CloudComputing #AmazonVPC #Networking #AmazonEC2 #DevOps #CloudLearning #AWSCloudJourney
