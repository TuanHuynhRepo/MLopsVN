# MLopsVN clone

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
#

# MLOps Marathon 2023 - Sample solution

This repository is the sample solution for MLOps Marathon 2023.

## Quickstart

1.  Prepare environment

    ```bash
    # Install python 3.9
    # Install docker version 20.10.17
    # Install docker-compose version v2.6.1
    pip install -r requirements.txt
    make mlflow_up
    ```

2.  Train model

    -   Download data, `./data/raw_data` dir should look like

        ```bash
        data/raw_data
        ├── .gitkeep
        └── phase-1
            └── prob-1
                ├── features_config.json
                └── raw_train.parquet
        ```

    -   Process data

        ```bash
        python src/data_processor.py --phase-id phase-1 --prob-id prob-1
        ```

    -   After processing data, `./data/train_data` dir should look like

        ```bash
        data/train_data
        ├── .gitkeep
        └── phase-1
            └── prob-1
                ├── category_index.pickle
                ├── test_x.parquet
                ├── test_y.parquet
                ├── train_x.parquet
                └── train_y.parquet
        ```

    -   Train model

        ```bash
        export MLFLOW_TRACKING_URI=http://localhost:5000
        python src/model_trainer.py --phase-id phase-1 --prob-id prob-1
        ```

    -   Register model: Go to mlflow UI at <http://localhost:5000> and register a new model named **phase-1_prob-1_model-1**

3.  Deploy model predictor

    -   Create model config at `data/model_config/phase-1/prob-1/model-1.yaml` with content:

        ```yaml
        phase_id: "phase-1"
        prob_id: "prob-1"
        model_name: "phase-1_prob-1_model-1"
        model_version: "1"
        ```

    -   Test model predictor

        ```bash
        # run model predictor
        export MLFLOW_TRACKING_URI=http://localhost:5000
        python src/model_predictor.py --config-path1 data/model_config/phase-1/prob-1/model-1.yaml --config-path2 data/model_config/phase-1/prob-2/model-1.yaml --port 8000

        # curl in another terminal
        curl -X POST http://localhost:8000/phase-1/prob-1/predict -H "Content-Type: application/json" -d @data/curl/phase-1/prob-1/payload-1.json

        # stop the predictor above
        ```

    -   Deploy model predictor

        ```bash
        make predictor_up
        make predictor_curl
        ```

    -   After running `make predictor_curl` to send requests to the server, `./data/captured_data` dir should look like:

        ```bash
         data/captured_data
         ├── .gitkeep
         └── phase-1
             └── prob-1
                 ├── 123.parquet
                 └── 456.parquet
        ```

4.  Improve model

    -   The technique to improve model by using the prediction data is described in `improve_model.md`.
    -   Label the captured data, taking around 3 minutes

        ```bash
        python3 src/label_auto.py --phase-id phase-1 --prob-id prob-1
        ```

    -   After label the captured data, `./data/captured_data` dir should look like:

        ```bash
        data/captured_data
        ├── .gitkeep
        └── phase-1
            └── prob-1
                ├── 123.parquet
                ├── 456.parquet
                └── processed
                    ├── captured_x.parquet
                    └── uncertain_y.parquet
        ```

    -   Improve model with updated data

        ```bash
        export MLFLOW_TRACKING_URI=http://localhost:5000
        python3 src/model_trainer.py --phase-id phase-1 --prob-id prob-1 --add-captured-data true
        ```

    -   Register model: Go to mlflow UI at <http://localhost:5000> and register model using the existing name **phase-1_prob-1_model-1**. The latest model version now should be `2`.

    -   Update model config at `data/model_config/phase-1/prob-1/model-1.yaml` to:

        ```yaml
        phase_id: "phase-1"
        prob_id: "prob-1"
        model_name: "phase-1_prob-1_model-1"
        model_version: "2"
        ```

    -   Deploy new model version

        ```bash
        make predictor_restart
        make predictor_curl
        ```

5.  Teardown

    ```bash
    make teardown
    ```
