import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction



def search_files(query):
    # Use GNOME Tracker for file search
    tracker_results = subprocess.check_output(['tracker', 'search', query]).decode('utf-8').split('\n')

    # Use Recoll for file search
    recoll_results = subprocess.check_output(['recoll', '-t', '-b', '-q', query]).decode('utf-8').split('\n')

    # Use Locate for file search
    locate_results = subprocess.check_output(['locate', query]).decode('utf-8').split('\n')

    # Combine and return results
    return tracker_results + recoll_results + locate_results

def handle_user_input(query):
    results = search_files(query)
    # Display results in uLauncher interface
    for result in results:
        print(result)  # Replace with code to display results in uLauncher

if __name__ == '__main__':
    # For testing purposes, handle user input from command line
    user_input = input("Enter search query: ")
    handle_user_input(user_input)
