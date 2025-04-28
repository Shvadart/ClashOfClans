# test_builder_status_live.py
import time
from builder_status import get_builder_status, wait_for_free_builder, builders_busy
from logger import log

time.sleep(4)

print(get_builder_status())