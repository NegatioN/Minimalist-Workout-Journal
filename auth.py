from aiohttp import web

class Authorization:
    def __init__(self, user, password):
        self.user_map = {user: password}

    async def check_credentials(self, username, password):
        saved_password = self.user_map.get(username)
        if not saved_password or saved_password != password:
            raise web.HTTPForbidden()

        return True

    async def authenticate(self, request):
        user = request.headers.get('user')
        password = request.headers.get('password')

        if user and password:
            return await self.check_credentials(username=user, password=password)
        else:
            raise web.HTTPForbidden()

