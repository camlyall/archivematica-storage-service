"""Configure S3

From here we can configure aspects of S3 in the Storage Service.
"""

from os import environ

from django.core.exceptions import ImproperlyConfigured

# Read and connect timeouts for S3. Ideally these will match the
# defaults recommended by your S3 implementation.
S3_TIMEOUTS = 900
try:
    S3_TIMEOUTS = int(environ.get("SS_S3_TIMEOUTS", S3_TIMEOUTS))
except ValueError:
    err_msg = "S3 timeout value configured incorrectly in the environment - please check the 'S3_TIMEOUTS' variable"
    raise ImproperlyConfigured(err_msg)

def _env_int(name, default):
    try:
        return int(environ.get(name, default))
    except ValueError as err:
        raise ImproperlyConfigured(
            f"{name} configured incorrectly in the environment"
        ) from err

TRUE_VALUES = {"1", "true", "yes", "on"}

def _env_bool(name, default):
    raw = environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in TRUE_VALUES

S3_TRANSFER_MAX_CONCURRENCY = _env_int("SS_S3_TRANSFER_MAX_CONCURRENCY", 1)
S3_TRANSFER_MULTIPART_THRESHOLD = _env_int(
    "SS_S3_TRANSFER_MULTIPART_THRESHOLD", 8 * 1024 * 1024
)
S3_TRANSFER_MULTIPART_CHUNKSIZE = _env_int(
    "SS_S3_TRANSFER_MULTIPART_CHUNKSIZE", 8 * 1024 * 1024
)
S3_TRANSFER_USE_THREADS = _env_bool("SS_S3_TRANSFER_USE_THREADS", False)
