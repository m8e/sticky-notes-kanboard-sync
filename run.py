from envparse import env, Env
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import arrow
import click
import platform
import os
import time


def debug(message, err=False, exit=False):
    click.echo('{} - {} - {}'.format(
        arrow.now(env('TIMEZONE')).format('MMM, D YYYY HH:mm:ss'),
        'ERR ' if err else 'INFO',
        message
    ), err=err)

    if exit:
        exit(1)


class StickyNoteFileHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        debug('Modified')

    def on_deleted(self, event):
        debug('Deleted')

    def on_moved(self, event):
        debug('Moved')


@click.command()
def run():
    Env.read_envfile('.env')

    debug('Initializing')

    platform_os = platform.system()
    platform_version = platform.release()
    sticky_notes_directory = None
    sticky_notes_filename = None
    sticky_notes_file_path = None

    if platform_os != 'Windows':
        debug('This script is only available on Windows Vista or above (for obvious reasons)', err=True, exit=True)

    if platform_version == 'Vista':
        debug('Not yet implemented', exit=True) # TODO
    elif platform_version == '7':
        debug('Not yet implemented', exit=True) # TODO
    elif platform_version == '8':
        debug('Not yet implemented', exit=True) # TODO
    elif platform_version == '10':
        sticky_notes_directory = os.path.join(env('USERPROFILE'), 'AppData\Roaming\Microsoft\Sticky Notes')
        sticky_notes_filename = 'StickyNotes.snt'
        sticky_notes_file_path = os.path.join(sticky_notes_directory, sticky_notes_filename)
    else:
        debug('Unable to determine the Windows version your are running, aborting', err=True, exit=True)

    debug('You are using Windows ' + platform_version)

    if not os.path.isfile(sticky_notes_file_path):
        debug('Sticky Notes file not found (should be at ' + sticky_notes_file_path + ')', err=True, exit=True)

    debug('Watching ' + sticky_notes_file_path)

    observer = Observer()
    observer.schedule(StickyNoteFileHandler(ignore_directories=True, patterns=[sticky_notes_filename]), path=sticky_notes_directory, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    run()