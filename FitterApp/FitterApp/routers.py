from rest_framework import routers
from map.api import *


router = routers.DefaultRouter(trailing_slash=True)


#user
router.register(r"register", RegisterViewSet, basename="register"),
router.register(r"login", LoginViewSet, basename="login"),
router.register(r"users", UserViewSet, basename="users"),

