class Linked_List:
    def __init__(self, key=None, value=None):
        self.value = value
        self.key = key # two-field list; non-standard realization
        self.next = None
        self.prev = None

    def insert_after(self, target): # insert target after self
        target.next = self.next
        target.prev = self
        if self.next is not None:
            self.next.prev = target
        self.next = target
        return target

    def insert_before(self, target): # insert target before self
        target.prev = self.prev
        target.next = self
        if self.prev is not None:
            self.prev.next = target
        self.prev = target
        return target

    def pop(self):
        _next = self.next
        _prev = self.prev
        if _next is not None:
             _next.prev = _prev
        if _prev is not None:
            _prev.next = _next
        self.next = None
        self.prev = None
        return self # return the entire node, albeit with links severed

    def set(self, value):
        self.value = value


class LFU_Cache:
    def __init__(self, capacity=10):
        try:
            if int(capacity) < 1:
                print('Cannot create a cache with no positive capacity')
                return None
        except ValueError:
            print('Capacity must be a (positive) number')
            return None

        self.first = Linked_List(None, True) # 'default' list nodes not keyed to anything;
        self.last = self.first.insert_after(Linked_List(None, False)) # there to call list methods from scratch

        self.capacity = capacity
        self.current_size = 0
        self.data = {} # data dict on keys, and (relative) frequencies

    def get(self, key):
        try:
            data = self.data[key]
            node = data['node']
            data['called'] += 1
            while (
            (node.prev is not None)
            and
            (node.prev.key is not None) # checks for the first node
            and
            data['called'] > self.data[node.prev.key]['called']):
                prev = node.prev
                prev.insert_before(node.pop())

            return node.value
        except KeyError:
            return None

    def set(self, key, value=None):
        try:
            data = self.data[key] # if already in cache
            data['node'].set(value) # set new value, no change in frequency
        except KeyError: # not yet in cache
            if self.current_size == self.capacity:
                obsolete = self.last.prev
                data = self.data.pop(obsolete.key)
                del data
                obsolete.pop()
                del obsolete
                self.current_size -= 1

            new = self.last.insert_before(Linked_List(key, value)) # add new node to the end
            self.data[key] = {'node': new, 'called': 0}
            self.current_size += 1

    def _del(self, key):
        try:
            data = self.data.pop(key)
            node = data['node'].pop()
            del data
            del node
            self.current_size -= 1
            return
        except KeyError:
            return # key not in cache, so what

    def list(self):
        print(self.current_size, '/', self.capacity)
        if self.current_size == 0:
            return
        else:
            cur = self.first.next
            while (cur != self.last):
                print(cur.key, cur.value, self.data[cur.key]['called'])
                cur = cur.next
            return
