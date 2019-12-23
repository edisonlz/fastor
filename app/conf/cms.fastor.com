upstream make_app {
    server 127.0.0.1:16000 fail_timeout=0;
}

server {
    listen 80;
    server_name cms.fastor.com;
    charset utf-8;

    location  /static/ {
        alias /data/python/one_platform/app/statics/;
        expires 15m;
    }

    location / {
        fastcgi_pass make_app;
        fastcgi_param PATH_INFO $fastcgi_script_name;
        fastcgi_param REQUEST_METHOD $request_method;
        fastcgi_param QUERY_STRING $query_string;
        fastcgi_param SERVER_NAME $server_name;
        fastcgi_param SERVER_PORT $server_port;
        fastcgi_param SERVER_PROTOCOL $server_protocol;
        fastcgi_param CONTENT_TYPE $content_type;
        fastcgi_param CONTENT_LENGTH $content_length;
        fastcgi_pass_header Authorization;
        fastcgi_intercept_errors off;
    }

}

