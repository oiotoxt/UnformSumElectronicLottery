## Run (Docker)

```bash
docker build -t tmp/lottery -f Dockerfile .

docker run -d --restart=unless-stopped --name lottery01 -p=8501:8501 tmp/lottery

docker logs -f -t lottery01
```

## License

개인 작업물이며, MIT License를 따릅니다.
