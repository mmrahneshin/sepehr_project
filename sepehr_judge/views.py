from django.shortcuts import render


# @api_view(["POST"])
# def login(request):
#     user = get_object_or_404(User, username=request.data["username"])
#     if not user.check_password(request.data["password"]):
#         return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
#     token, created = Token.objects.get_or_create(user=user)
#     serializer = UserSerializer(instance=user)
#     return Response({"token": token.key, "user": serializer.data})


# @api_view(["POST"])
# def signup(request):
#     # serializer = UserSerializer(data=request.data)
#     # if serializer.is_valid():
#     #     serializer.save()

#     return Response({})


# @api_view(["GET"])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     return Response("passed for {}".format(request.user.email))
