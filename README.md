# MLopsVN

## Prepare to run on service cloud EC2 of AWS

1. Install git skip if install

    ```bash
    #Perform a quick update on your instance:
    sudo yum update -y
 
    #Install git in your EC2 instance
    sudo yum install git -y
 
    #Check git version
    git version
    ```

2. Install python skip if install
    ```bash
    sudo yum install python3 -y
    ```

3. Install docker
    ```bash
    #Update the installed packages and package cache on your instance:
    sudo yum update -y

    #Install the most recent Docker Engine package:
    sudo amazon-linux-extras install docker
    #or
    sudo snap install docker

    #Start the Docker service:
    sudo service docker start
    
    #(Optional)
    sudo systemctl enable docker

    #Add the ubuntu to the docker group so you can execute Docker commands without using sudo:
    #1. Create group docker
    sudo groupadd docker
    #2. Add user
    sudo usermod -a -G docker ubuntu
    #or
    sudo usermod -aG docker $USER

    #Log out and log back EC2
    #Verify that you can run Docker commands without sudo:
    docker info
    ```
4. Install docker-compose
    ```bash
    #Download Docker-compose:
    sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    
    #Fix permissions after download:
    sudo chmod +x /usr/local/bin/docker-compose
    
    #Vetify success:
    docker-compose version
    ```
5. Clone repository
    ```bash
    git clone https://github.com/HT-Tuan/MLopsVN.git
    ```
