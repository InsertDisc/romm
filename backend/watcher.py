import os
from datetime import timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from endpoints.scan import scan_platforms
from utils.redis import low_prio_queue
from logger.logger import log

from config import (
    HIGH_PRIO_STRUCTURE_PATH,
    LIBRARY_BASE_PATH,
    ENABLE_RESCAN_ON_FILESYSTEM_CHANGE,
    RESCAN_ON_FILESYSTEM_CHANGE_DELAY,
)

path = (
    HIGH_PRIO_STRUCTURE_PATH
    if os.path.exists(HIGH_PRIO_STRUCTURE_PATH)
    else LIBRARY_BASE_PATH
)


class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not ENABLE_RESCAN_ON_FILESYSTEM_CHANGE:
            return

        # Ignore .DS_Store files
        if event.src_path.endswith(".DS_Store"):
            return

        # Ignore modified events
        if event.event_type == "modified":
            return

        event_src = event.src_path.split(path)[-1]
        platform_slug = event_src.split("/")[1]
        time_delta = timedelta(minutes=RESCAN_ON_FILESYSTEM_CHANGE_DELAY)

        log.info(f"Filesystem event: {event.event_type} {event_src}")

        low_prio_queue.scheduled_job_registry.remove_jobs()

        # Skip if a scan is already scheduled
        for job_id in low_prio_queue.scheduled_job_registry.get_job_ids():
            job = low_prio_queue.fetch_job(job_id)
            if (
                job
                and job.is_scheduled
                and job.func_name == "endpoints.scan.scan_platforms"
            ):
                if job.args[0] == []:
                    log.info("Full rescan already scheduled")
                    return

                if platform_slug in job.args[0]:
                    log.info(f"Scan already scheduled for {platform_slug}")
                    return

        rescan_in_msg = f"rescanning in {RESCAN_ON_FILESYSTEM_CHANGE_DELAY} minutes."

        # # Any change to a platform directory should trigger a full rescan
        if event.is_directory and event_src.count("/") == 1:
            log.info(f"Platform directory changed, {rescan_in_msg}")
            return low_prio_queue.enqueue_in(time_delta, scan_platforms, [])

        # Otherwise trigger a rescan for the specific platform
        log.info(f"Change detected in {platform_slug} folder, {rescan_in_msg}")
        return low_prio_queue.enqueue_in(
            time_delta,
            scan_platforms,
            [platform_slug],
        )


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(EventHandler(), path, recursive=True)
    observer.start()

    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()
