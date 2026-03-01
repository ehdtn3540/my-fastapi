import httpx

# 공유할 클라이언트를 담을 클래스 혹은 변수
class HttpClient:
    client: httpx.AsyncClient = None

http_client = HttpClient()
