from auth_app.models import Account
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import OfferSerializer, OfferDetailsSerializer, OfferListSerializer, OfferListSingleSerializer, OfferSinglePatchSerializer
from offers_app.models import Offer, OfferDetail
from django.core.paginator import Paginator
from .filters import apply_offer_filters, apply_offer_ordering

"""List or create offers."""
class OffersView(APIView):
    permission_classes = [AllowAny]
    
    # List offers with filtering, ordering, and pagination.
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

    # Create a new offer (business users only).
    def post(self, request):
        if request.user.user_type != Account.BUSINESS:
            return Response({"detail": "Only business users are allowed to write offers."}, status=status.HTTP_403_FORBIDDEN)    

        serializer = OfferSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                offer = serializer.save()
                return Response(OfferSerializer(offer).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""Retrieve, update, or delete a single offer."""
class OfferSingleView(APIView):
    permission_classes = [IsAuthenticated]

    # Retrieve a single offer by ID.
    def get(self, request, id):
        try:
            offer = Offer.objects.prefetch_related('details').select_related('user').get(pk=id)
            serializer = OfferListSingleSerializer(offer, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Offer.DoesNotExist:
            return Response({'error': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Update a single offer by ID (owner only).
    def patch(self, request, id):
        try:
            offer = Offer.objects.get(pk=id)
        except Offer.DoesNotExist:
            return Response({"detail": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OfferSinglePatchSerializer(offer, data=request.data, partial=True, context={'request': request})
        
        if request.user.business_user != offer.business_user:
            return Response({"detail": "Only the owner can update this Offer."}, status=status.HTTP_403_FORBIDDEN)  
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a single offer by ID (owner only).
    def delete(self, request, id):
        try:
            offer = Offer.objects.get(pk=id)
        except Offer.DoesNotExist:
            return Response({"detail": "Offer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user.id != offer.user_id:
            return Response({"detail": "Only the owner can delete this Offer."}, status=status.HTTP_403_FORBIDDEN)

        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

"""Retrieve a single offer detail."""
class OfferDetailView(APIView):
    permission_classes = [AllowAny]
    
    # Get offer detail by ID.
    def get(self, request, id):
        try:
            offer_detail = OfferDetail.objects.get(pk=id)
        except OfferDetail.DoesNotExist:
            return Response({"detail": "OfferDetail not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OfferDetailsSerializer(offer_detail, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)