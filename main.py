from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import subprocess

class FileSearchExtension(Extension):
    def __init__(self):
        super(FileSearchExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument()
        if query:
            results = search_files(query)
            return RenderResultListAction(results)
        else:
            return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                               name='File Search',
                                                               description='Enter a search query to find files',
                                                               on_enter=HideWindowAction())])

def search_files(query):
    # Use GNOME Tracker for file search
    tracker_results = subprocess.check_output(['tracker', 'search', query]).decode('utf-8').split('\n')

    # Use Recoll for file search
    recoll_results = subprocess.check_output(['recoll', '-t', '-b', '-q', query]).decode('utf-8').split('\n')

    # Use Locate for file search
    locate_results = subprocess.check_output(['locate', query]).decode('utf-8').split('\n')

    # Combine and return results
    all_results = tracker_results + recoll_results + locate_results
    return [ExtensionResultItem(icon='images/icon.png', name=result, on_enter=HideWindowAction()) for result in all_results if result]

if __name__ == '__main__':
    FileSearchExtension().run()
