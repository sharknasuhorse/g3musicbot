# g3musicbot


## usage

1. git clone

2. cd  
`cd g3musicbot`

3. copy config  
    ```
    cp src/config/example_options.ini src/config/options.ini
    cp src/config/example_aliases.json src/config/aliases.json
    cp src/config/example_permissions.ini src/config/permissions.ini
    ```

4. edit src/config/options.ini

    ```
    Token = bot_token
    DevIDs = userid
    ```
5. edit docker-compose.yml
    ```
    environment:
    - ADMIN_PASS=hogehogehoge
    ```

6. docker build  
`docker build . -t g3musicbot:master`

7. docker-compose up  
`docker-compose up -d`
