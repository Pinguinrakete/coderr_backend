from django.db.models import Q

# Apply filtering to offers queryset based on query parameters.
def apply_offer_filters(queryset, params):
    creator_id = params.get('creator_id')
    if creator_id:
        queryset = queryset.filter(business_user=creator_id)

    min_price = params.get('min_price')
    if min_price:
        queryset = queryset.filter(details__price__gte=min_price)

    max_delivery_time = params.get('max_delivery_time')
    if max_delivery_time:
        queryset = queryset.filter(details__delivery_time_in_days__lte=max_delivery_time)

    search = params.get('search')
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    return queryset

# Order offers queryset by updated_at or min_price.
def apply_offer_ordering(queryset, ordering_param):
    if ordering_param:
        if ordering_param == 'updated_at':
            return queryset.order_by('updated_at')
        elif ordering_param == 'min_price':

            return sorted(
                queryset,
                key=lambda o: min([d.price for d in o.details.all()]) if o.details.exists() else float('inf')
            )

    return queryset.order_by('-updated_at')