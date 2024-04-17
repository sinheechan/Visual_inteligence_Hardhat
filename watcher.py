import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os

def delete(path):
    for f in os.listdir(path):  # 디렉토리를 조회한다
        f = os.path.join(path, f)
        if os.path.isfile(f):  # 파일이면
            try:
                os.remove(f)  # 파일을 지운다
                print(f, 'is deleted')  # 삭제완료 로깅
            except OSError:  # Device or resource busy (다른 프로세스가 사용 중)등의 이유
                print(f, 'can not delete')  # 삭제불가 로깅           
    
class Target:
    watchDir = os.getcwd()
    watchDir = 'C:\\Users\\leesc\\PycharmProjects\\YOLOv8API\\runs\\detect\\'
    #watchDir에 감시하려는 디렉토리를 명시한다.

    def __init__(self):
        self.observer = Observer()   #observer객체를 만듦

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, 
                                                       recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(0.1)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):
#FileSystemEventHandler 클래스를 상속받음.
#아래 핸들러들을 오버라이드 함
    #파일, 디렉터리가 move 되거나 rename 되면 실행
    '''
    def on_moved(self, event):
        print(event)
    '''
    def on_created(self, event): #파일, 디렉터리가 생성되면 실행
        print(event)
        #shutil.rmtree(Target.watchDir, ignore_errors=True, onerror=delete(Target.watchDir))
        delete('C:\\Users\\leesc\\PycharmProjects\\YOLOv8API\\runs\\detect\\')
    '''
    def on_deleted(self, event): #파일, 디렉터리가 삭제되면 실행
        print(event)
    def on_modified(self, event): #파일, 디렉터리가 수정되면 실행
        print(event)
    '''
if __name__ == "__main__": #본 파일에서 실행될 때만 실행되도록 함
    w = Target()
    w.run()
