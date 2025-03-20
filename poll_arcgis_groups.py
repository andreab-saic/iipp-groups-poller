import os
import time
import redis
from arcgis.gis import GIS
from dotenv import load_dotenv

# Load environment variables
def load_envs():
    load_dotenv()

def get_env(key):
    return os.environ.get(key)

# Load environment variables
load_envs()

ARCGIS_CLIENT_URL    = get_env('ARCGIS_CLIENT_URL')
ARCGIS_CLIENT_ID     = get_env('ARCGIS_CLIENT_ID')
ARCGIS_CLIENT_SECRET = get_env('ARCGIS_CLIENT_SECRET')
REDIS_SERVER         = get_env('REDIS_SERVER')

# Initialize ArcGIS GIS object
gis = GIS(ARCGIS_CLIENT_URL, ARCGIS_CLIENT_ID, ARCGIS_CLIENT_SECRET, use_gen_token=True)

# Initialize Redis client with SSL enabled
redis_client = redis.Redis(
    host=REDIS_SERVER,
    port=6379,
    db=0,
    decode_responses=True,
    ssl=True,  # Enable SSL explicitly
    ssl_cert_reqs=None,  # Disable certificate verification (safe in AWS)
    socket_timeout=10,  # Increase timeout for slow responses
    socket_connect_timeout=10,
    retry_on_timeout=True,
    health_check_interval=30,  # Automatically check connection health
)

def get_arcgis_groups():
    """Retrieve group titles from ArcGIS."""
    groups = gis.groups.search(max_groups=10000)
    group_titles = [group.title for group in groups]
    return group_titles

def cache_group_titles_in_redis(group_titles):
    """Cache group titles in Redis."""
    redis_key = "arcgis_groups"
    redis_client.set(redis_key, str(group_titles))  # Store as a string
    print(f"Group titles cached in Redis with key: {redis_key}")

def main():
    """Main function to fetch groups and cache them in Redis."""
    group_titles = get_arcgis_groups()
    cache_group_titles_in_redis(group_titles)

if __name__ == "__main__":
    main()

