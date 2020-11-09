## Run (Docker)

```bash
docker build -t tmp/lottery -f Dockerfile .

docker run -d --restart=unless-stopped --name lottery01 -p=8501:8501 tmp/lottery
```


```bash
pip install gunicorn
gunicorn  --bind 0.0.0.0:8501 app_dash:server
```

```
ssh -i meta.keypair.cloud.ncsoft.com.pem ubuntu@172.19.149.225

ssh -i meta.keypair.cloud.ncsoft.com.pem ubuntu@172.19.151.82

ssh -i meta.keypair.cloud.ncsoft.com.pem ubuntu@172.19.148.94 <== 사내 오픈
접속붉가
172.18.56.0/22


https://github.com/oiotoxt/UniformSumLottery
```
