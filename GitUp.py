import os

from SaveIO import IoString as IoString

class GitUp(IoString):

    def __init__(self, git_project):
        super().__init__(git_project)

    def write(self, a_string)->bool:
        return super().save_out(a_string)
    
    def read(self)->str():
        return super().read_latest()

    def download(self)->bool:
        state = self._git_pull()
        return state

    def upload(self, message)->bool:
        state = self._git_add()
        if state:
            state = self._git_commit(message)
        if state == True:
            state = self._git_push()
        return state

    def _git_pull(self)->int:
        return self._git_exec(['pull'])

    def _git_add(self)->int:
        return self._git_exec(['add', f"*{self.file_type}"])

    def _git_commit(self, message)->bool:
        return bool(self._git_exec(['commit', message]))

    def _git_push(self)->bool:
        return bool(self._git_exec(['push']))

    def _git_exec(self, params)->int:
        commands = 'git '
        op = params[0]
        commands += op
        commands += ' '
        if op == 'commit':
            commands += '-m "'
            commands += params[1]
            commands += '"'
        else:
            for param in params[1:]:
                commands += ' '
                commands += param
        success = False
        pwd = os.getcwd()
        try:
            os.chdir(self.git_folder)
            if os.getcwd() != self.git_folder:
                raise Exception(f"Error: Unable to change to [{self.git_folder}]")
            with os.popen(commands.strip()) as proc:
                print(*proc)
            success = True
        except Exception as ex:
            os.chdir(pwd)
            print(ex)
        return success
    

if __name__ == '__main__':
    TEST_MESSAGE = 'nagy'
    test = GitUp(os.getcwd())
    if not test.download():
        raise Exception("Error: Unble to pull remote files.")
    if not test.write(TEST_MESSAGE):
        raise Exception("Unable to save file.")
    if not test.upload("Test case 2"):
        raise Exception("Unable to sync file.")
    results = test.read()
    if results != TEST_MESSAGE:
        raise Exception("Unable to read file.")
    results = test.list_all()
    if not results:
        raise Exception("Unable to list file.")
    success = False
    if len(results):
        test.remove_all_files()
        if not test.list_all():
            print("Testing success.")
            success = True
    if not success:
        print("Error: Regression.")
        

