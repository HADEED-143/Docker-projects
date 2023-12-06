from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Worker
from .serializer import CustomUserSerializer, WorkerSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    try:
        if request.user:
            user = CustomUser.objects.get(id=request.user.id)
            user_serializer = CustomUserSerializer(user)
            return Response(user_serializer.data)
        else:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_info_single(request, user_id):
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(id=user_id)
            user_serializer = CustomUserSerializer(user)
            return Response(user_serializer.data)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'PATCH':

        try:
            # Get the authenticated user and check permissions
            authenticated_user = request.user
            requested_user = CustomUser.objects.get(id=user_id)

            # Make the request.data mutable so that we can pop the profile_picture field
            request.data._mutable = True

            if authenticated_user.id != user_id:
                return Response({'detail': 'You do not have permission to update this user.'}, status=status.HTTP_403_FORBIDDEN)

            # check if the profile picture is provided as link or file
            if 'profile_picture' in request.data:
                profile_picture = request.data['profile_picture']
                # Check if the profile picture is a file (not a URL)
                if isinstance(profile_picture, InMemoryUploadedFile):
                    requested_user.profile_picture = profile_picture
                else:
                    # don't change the profile picture if it's a URL
                    request.data.pop('profile_picture')

            # Create a serializer instance with both user data and uploaded files
            serializer = CustomUserSerializer(
                requested_user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# search worker with filters and pagination
@api_view(['GET'])
def search_workers(request):
    query = request.GET.get('query')
    filters = request.GET.get('filters')

    # Start with all workers
    workers = Worker.objects.all()

    # Apply search query
    if query:
        workers = workers.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(skills__icontains=query)
        )

    # Apply filters
    if filters:
        filter_params = filters.split(',')
        for param in filter_params:
            field, value = param.split(':')
            if '__' in field:
                field, lookup = field.split('__')
                workers = workers.filter(**{f'{field}__{lookup}': value})
            else:
                workers = workers.filter(**{field: value})

    # Paginate the queryset
    paginator = PageNumberPagination()
    paginator.page_size = 15  # Set your desired page size here
    paginated_workers = paginator.paginate_queryset(workers, request)

    # Serialize the paginated queryset
    serializer = WorkerSerializer(paginated_workers, many=True)

    # Return paginated response
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def view_or_update_worker_information(request, id):
    if request.method == 'GET':
        try:
            worker = Worker.objects.get(user_id=id)
            serializer = WorkerSerializer(worker)
            return Response(serializer.data)
        except Worker.DoesNotExist:
            return Response({'detail': 'Worker not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'PATCH':
        try:
            # Get the authenticated user and check permissions
            authenticated_user = request.user
            requested_worker = Worker.objects.get(user_id=id)

            if authenticated_user.id != id:
                return Response({'detail': 'You do not have permission to update this worker.'}, status=status.HTTP_403_FORBIDDEN)

            # Create a serializer instance with both user data and uploaded files
            serializer = WorkerSerializer(
                requested_worker, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Worker.DoesNotExist:
            return Response({'detail': 'Worker not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def ping(request):
    return Response({'detail': 'pong'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_password(request):
    user = request.user

    current_password = request.data.get('currentPassword')
    new_password = request.data.get('newPassword')
    re_new_password = request.data.get('confirmPassword')

    # Check if the current password matches
    if not check_password(current_password, user.password):
        return Response({"detail": "Current password is incorrect."}, status=400)

    # Check if the new password and re_new_password match
    if new_password != re_new_password:
        return Response({"detail": "New passwords do not match."}, status=400)

    # Validate the new password
    try:
        validate_password(new_password)
    except Exception as e:
        return Response({"detail": str(e)}, status=400)

    # Update the user's password
    user.set_password(new_password)
    user.save()

    return Response({"detail": "Password reset successfully."}, status=200)
