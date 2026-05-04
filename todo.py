class Task:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name
 

if __name__== "__main__":
    task = Task("write program")
    print(task.get_name())

