#!/usr/bin/env python3
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import os
from threading import Thread, Lock


class FileWatcher:
    def __init__(self, path, recursive, on_create, on_move, on_delete, on_modify):
        self.__event_handler = FileSystemEventHandler()
        self.__event_handler.on_created = on_create
        self.__event_handler.on_deleted = on_delete
        self.__event_handler.on_modified = on_modify
        self.__event_handler.on_moved = on_move
        self.__observer = Observer()
        self.__observer.schedule(self.__event_handler, path, recursive=recursive)

    def start(self):
        print("starting filewatcher")
        self.__enabled = True
        self.__service = Thread(target=self.__service_logic, args=[])
        self.__service.daemon = True
        self.__service.start()


    def stop(self):
        print("stopping filewatcher")
        self.__enabled = False
        self.__service.join()


    def __service_logic(self):
        # start observer
        self.__observer.start()
        try:
            while self.__enabled:
                time.sleep(1)
        except Exception as ex:
            print("stopping cuz: ", ex)
            self.__enabled = False
        finally:
            self.__observer.stop()
            self.__observer.join()


class ExampleRuleWatcher:
    def __init__(self, src_path):
        self.__path = src_path
        self.__mutex = Lock()
        self.__rule_cache = dict()
        self.__file_watcher = FileWatcher(
            path=src_path,
            recursive=True,
            on_create=self.__create_handler(),
            on_move=self.__delete_handler(),
            on_delete=self.__delete_handler(),
            on_modify=self.__modify_handler())

    def start(self):
        self.__load_rules()
        self.__file_watcher.start()

    def stop(self):
        self.__file_watcher.stop()


    def read_cache(self):
        ret = None
        self.__mutex.acquire()
        try:
            ret = self.__rule_cache
        finally:
            self.__mutex.release()
        return ret
    
    def __cache_action(self, action, args):
        self.__mutex.acquire()
        try:
            action(args)
        except Exception as ex:
            print("could not perform cache action: " + str(action) + " args: " + str(args) + " : ", ex)
        finally:
            self.__mutex.release()
    
    def __update_action(self, args):
        path = args[0]
        fh = args[1]
        data = json.load(fh)
        self.__rule_cache[path] = data
    
    def __delete_action(self, args):
        path = args[0]
        del self.__rule_cache[path]

    def __is_rule_event(self, event):
        if event.is_directory:
            return False
        
        file_path = event.src_path
        if not file_path.endswith(".json"):
            return False
        
        return True
    
    def __load_rules(self):
        for root, d_names, f_names, in os.walk(self.__path):
            for f in filter(lambda x: x.endswith(".json"), f_names):
                file_path = os.path.join(root, f)
                file_path = os.path.abspath(file_path)
                print("loading " + file_path)
                with open(file_path) as rule_file:
                    self.__cache_action(self.__update_action, args=[file_path, rule_file])

    def __modify_handler(self):
        def handler(event):
            if not self.__is_rule_event(event):
                return 

            print("Rule modified")
            file_path = event.src_path
            with open(file_path) as rule_file:
                self.__cache_action(self.__update_action, args=[file_path, rule_file])

        return handler

    def __create_handler(self):
        def handler(event):
            if not self.__is_rule_event(event):
                return 

            print("Rule created")
            file_path = event.src_path
            with open(file_path) as rule_file:
                self.__cache_action(self.__update_action, args=[file_path, rule_file])

        return handler
    
    def __delete_handler(self):
        def handler(event):
            if not self.__is_rule_event(event):
                return 

            print("Rule deleted/moved")
            file_path = event.src_path
            self.__cache_action(self.__delete_action, args=[file_path])            

        return handler
    
if __name__ == "__main__":
    print("testing things here")
    test = ExampleRuleWatcher("./rules")
 

    test.start()
    for x in range(1, 50):
        print("cache: " + json.dumps(test.read_cache(), indent=2))
        time.sleep(1)
    test.stop()

        