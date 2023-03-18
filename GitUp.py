from SaveIO import IoString as IoString

class GitUp(IoString):

    def __init__(self, git_project):
        super().__init__(git_project)

    def write(astring)->bool:
        pass
    
    def read(self)->str():
        pass

    def sync(self)->bool:
        pass
    

if __name__ == '__main__':
    test = GitUp('.')
    test.remove_all_files()
    if not test.save_out('nagy'):
        raise Exception("Unable to save file.")
    results = test.read_latest()
    print(results)
    if results != 'nagy':
        raise Exception("Unable to read file.")
    results = test.list_all()
    if not results:
        raise Exception("Unable to list file.")
    success = False
    if len(results) == 1:
        test.remove_all_files()
        if not test.list_all():
            print("Testing success.")
            success = True
    if not success:
        print("Error: Regression.")
        

