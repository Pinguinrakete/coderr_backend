from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import OfferSerializer, OfferDetailsSerializer, OfferListSerializer, OfferListSingleSerializer, OfferSinglePatchSerializer, ImageUploadSerializer
from offers_app.models import Offer, OfferDetail
from django.core.paginator import Paginator
from .filters import apply_offer_filters, apply_offer_ordering

"""
Handles listing and creation of service offers.

Permissions: 
- Requires authentication (IsAuthenticated)

Methods:

GET:
- Retrieves a paginated list of offers.
- Supports filtering and sorting via query parameters.

Query Parameters:
- ordering (str, optional): Specifies the sorting field, e.g., `price`, `-created_at`, etc.
- page (int, optional): Page number for pagination. Default: 1.
- page_size (int, optional): Number of offers per page. Default: 6.
- Additional custom filters may be supported depending on `apply_offer_filters`.

Returns:
- count (int): Total number of offers.
- next (str or null): URL to the next page of results.
- previous (str or null): URL to the previous page of results.
- results (list): Serialized list of offers.

Errors:
- 400: Invalid filter, ordering, or pagination input.
- 404: Page number out of valid range.
- 500: Unexpected server error.

---

POST:
- Creates a new service offer.

Accepts:
- title (str): Title of the offer.
- image (file, optional): Image representing the offer.
- description (str, optional): Text description.
- details (list): List of OfferDetail IDs or embedded detail data.
- business_user (int): ID of the associated business user.

Returns:
- The created offer in serialized format on success.

Errors:
- 400: Validation errors in the submitted data.
- 500: Unexpected error during creation.
"""
class OffersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            offers = Offer.objects.prefetch_related('details').select_related('user')

            try:
                offers = apply_offer_filters(offers, request.query_params)
            except Exception as e:
                return Response({'error': f'Error while filtering the offers: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

            ordering = request.query_params.get('ordering')
            try:
                offers = apply_offer_ordering(offers, ordering)
            except Exception as e:
                return Response({'error': f'Error while sorting the offers: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                page_size = int(request.query_params.get('page_size', 6))
                page = int(request.query_params.get('page', 1))
            except ValueError:
                return Response({'error': 'Invalid value for page or page_size. Both must be integers.'}, status=status.HTTP_400_BAD_REQUEST)

            paginator = Paginator(offers, page_size)
            try:
                paged_offers = paginator.page(page)
            except PageNotAnInteger:
                return Response({'error': 'Page number is not a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)
            except EmptyPage:
                return Response({'error': 'The requested page is empty or out of the valid range.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = OfferListSerializer(paged_offers, many=True)

            base_url = request.build_absolute_uri('?').split('?')[0]
            next_url = f'{base_url}?page={page + 1}' if paged_offers.has_next() else None
            prev_url = f'{base_url}?page={page - 1}' if paged_offers.has_previous() else None

            return Response({
                'count': paginator.count,
                'next': next_url,
                'previous': prev_url,
                'results': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = OfferSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                offer = serializer.save()
                return Response(OfferSerializer(offer).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                import traceback
                print(traceback.format_exc()) 
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
Handles retrieval, partial update, and deletion of a single service offer.

Permissions:
- Requires authentication (IsAuthenticated)
- Delete (and optionally update) restricted to the offer owner

Methods:

GET:
- Retrieves the details of a single offer by its ID.
- Includes related user and offer details in the response.

Path Parameters:
- id (int): Primary key of the offer to retrieve.

Returns:
- Serialized offer data with related details.
- 200 on success.
- 404 if the offer does not exist.
- 500 on unexpected errors.

PATCH:
- Partially updates an existing offer.
- Only authenticated users can perform this.
- (Optionally) Only the offer owner should be allowed to update.

Accepts:
- Partial data to update fields of the offer.

Path Parameters:
- id (int): Primary key of the offer to update.

Returns:
- Serialized updated offer data on success.
- 400 on validation errors.
- 403 if the user is not the owner (if ownership check implemented).
- 404 if the offer does not exist.

DELETE:
- Deletes an offer by its ID.
- Only the offer owner is authorized to delete.

Path Parameters:
- id (int): Primary key of the offer to delete.

Returns:
- 204 No Content on successful deletion.
- 403 if the user is not the owner.
- 404 if the offer does not exist.
"""
class OfferSingleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            offer = Offer.objects.prefetch_related('details').select_related('user').get(pk=id)
            serializer = OfferListSingleSerializer(offer, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Offer.DoesNotExist:
            return Response({'error': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, id):
        try:
            offer = Offer.objects.get(pk=id)
        except Offer.DoesNotExist:
            return Response({"detail": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OfferSinglePatchSerializer(offer, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            offer = Offer.objects.get(pk=id)
        except Offer.DoesNotExist:
            return Response({"detail": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.id != offer.user_id:
            return Response({"detail": "Only the owner can delete this Offer."}, status=status.HTTP_403_FORBIDDEN)

        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
"""
Handles retrieval of a single offer detail.

Permissions:
- Allows any user (authenticated or not) to access.

Methods:

GET:
- Retrieves the details of a single offer detail by its ID.

Path Parameters:
- id (int): Primary key of the offer detail to retrieve.

Returns:
- Serialized offer detail data.
- 200 on success.
- 404 if the offer detail does not exist.
"""
class OfferDetailsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, id):
        try:
            offer_detail = OfferDetail.objects.get(pk=id)
        except OfferDetail.DoesNotExist:
            return Response({"detail": "OfferDetail not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OfferDetailsSerializer(offer_detail, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
Handles partial updates to upload or update an image for an existing offer.

Permissions:
- Allows any user (authenticated or not) to access.

Methods:

PATCH:
- Updates the image of a specified offer.

Accepts:
- id (int): ID of the offer to update.
- image (file): The image file to upload or update.

Request Data:
- The `id` field is required to identify the offer.
- Partial update is supported (only the image needs to be provided).

Returns:
- Serialized updated offer data including the new image on success.
- 200 on successful update.
- 400 if the `id` is missing or validation fails.
- 404 if the offer with the given ID does not exist.
"""
class ImageUploadView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, format=None):
        offer_id = request.data.get('id')
        if not offer_id:
            return Response({"detail": "Image ID not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            offer = Offer.objects.get(pk=offer_id)
        except Offer.DoesNotExist:
            return Response({"detail": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ImageUploadSerializer(offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)