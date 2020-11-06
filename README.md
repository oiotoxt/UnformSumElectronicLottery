## Run (Docker)

```bash
docker build -t tmp/lottery -f Dockerfile .

docker run -d --restart=unless-stopped --name lottery01 -p=8501:8501 tmp/lottery
```
