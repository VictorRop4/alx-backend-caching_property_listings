from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Retrieve all properties from cache if available.
    Otherwise, fetch from the database and cache for 1 hour.
    """
    properties = cache.get('all_properties')
    if properties is None:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour
    return properties

import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss statistics and compute the hit ratio.
    Returns a dictionary with metrics.
    """
    conn = get_redis_connection("default")
    info = conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),  # 2 decimal places
    }

    logger.info(f"Redis Cache Metrics: {metrics}")
    return metrics
