# g3musicbot


## usage

1. git clone

2. cd  
`cd g3musicbot`

3. copy config  
`cp config/example_options.ini config/options.ini`

4. edit config/options.ini

    ```
    Token = bot_token
    DevIDs = userid
    ```

5. docker build  
`docker build . -t g3musicbot:master`

6. docker-compose up  
`docker-compose up -d`