from ninja import NinjaAPI, Schema

api = NinjaAPI()


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    email: str = None
    first_name: str = None
    last_name: str = None


@api.get("/hello")
def hello(request):
    return "Hello world"


@api.get("/me", response=UserSchema)
def me(request):
    return request.user
