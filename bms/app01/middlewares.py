from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.core.cache import cache


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        xxx = request.COOKIES.get('xxx')
        path = request.path_info
        print(path, xxx)
        if path == '/app01/vip' and xxx != 'QWERT':
            return redirect('/app01/login')
        res = self.get_response(request)

        return res


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 限制每个IP地址的请求频率为10次/分钟
        ip_address = request.META.get('REMOTE_ADDR')
        key = f'rate_limit:{ip_address}'
        limit = 10
        timeout = 60

        # 检查请求频率是否超过限制
        count = cache.get(key, 0)
        if count >= limit:
            return HttpResponse('请求频率超过限制，请稍后再试。')
        else:
            # 增加请求计数器，并设置过期时间
            cache.set(key, count + 1, timeout)
            return self.get_response(request)
