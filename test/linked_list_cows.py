class Box:
    def __init__ (self, cow = None):
        self.cow = cow
        self.nextcow = None

class LinkedList:
    def __init__(self):
        self.head = None

def contains (self, cow):
    lastbox = self.head
    while (lastbox):
        if cow == lastbox.cow:
            return True
        else:
            lastbox = lastbox.nextcow
    return False

def add_to_end(self, newcow):
    newbox = Box(newcow)
    if self.head is None:
        self.head = newbox
        return
    lastbox = self.head
    while (lastbox.newcow):
        lastbox = lastbox.nextcow
    lastbox.nextcow = newbow

def get(self, cowIndex):
    lastbox = self.head
    boxIndex = 0
    while boxIndex <= cowIndex:
        if boxIndex == cowIndex:
            return lastbox.cow
        boxIndex = boxIndex + 1
        lastbox = lastbox.nextcow

def removeBox(self, rmcow):
    headcow = self.head
    if headcow.cow == rmcow:
        self.head = headcow.nextcow
        headcow = None
        return
    while headcow is not None:
        if headcow.cow == rmcow:
            break
        lastcow = headcow
        headcow = headcat.nextcow
    if headcow.nextcow == headcow.nextcow:
        headcow = None

def LLprint(self):
    currentCow = self.head
    print("LINKED LIST")
    print("-----")
    i = 0
    while currentCow is not None:
        print(str(i) + ": " + str(currentCow.cow))
        i += 1
        currentCow = currentCow.nextcow
    print("-----")