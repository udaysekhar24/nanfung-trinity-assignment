###
# LRU Cache can be implemented using a dict(cache) and DoublyLinkedList(DLL)
# methods:
#   get(key):
#       Search key in cache
#           Yes: Set key as HEAD in DLL and return contents
#           No: return None
#   -------------------------------
#   put(key, content):
#       Search key in cache
#           Yes: Update content and set node to HEAD
#           No:
#               Check if size of cache is not maximum
#                   Yes: Add node to cache and set it to HEAD
#                   No: Remove TAIL node and Add node to cache and set it to HEAD
###


class DoublyLinkedListNode:
    def __init__(self, key, value):
        self.cache_key = key
        self.content = value
        self.next = None
        self.prev = None


class LRUCache:

    # initialize capacity and DLL head and tail.
    def __init__(self, size: int):
        self.size = size
        self.cache = dict()
        self.head = DoublyLinkedListNode(None, None)
        self.tail = DoublyLinkedListNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    # print the current state of LRUCache
    def __str__(self):
        return """ 
        LRU:
            Cache: {cache} 
            DLL Head: {head}
            DLL Tail: {tail}
        """.format(cache=self.cache.keys(),
                   head=self.head.next.cache_key,
                   tail=self.tail.prev.cache_key)

    # add node to the head of DLL.
    def add_node_to_head(self, dll_node):
        dll_node.next = self.head.next
        dll_node.next.prev = dll_node
        dll_node.prev = self.head
        self.head.next = dll_node

    # delete given node
    def delete_node(self, dll_node):
        dll_node.prev.next = dll_node.next
        dll_node.next.prev = dll_node.prev

    def get(self, search_key):
        # Look up the item in our cache
        # If the search item in cache then return
        if search_key in self.cache:
            # Search in our map and return
            search_node = self.cache[search_key]
            result_content = search_node.content
            # set accessed item to head
            self.delete_node(search_node)
            self.add_node_to_head(search_node)
            # print("After get({key})".format(key=search_key))
            # print(self)
            return result_content
        # print("*****Key:{key} not found*****".format(key=search_key))
        return None

    def put(self, key, value):
        if self.cache.get(key):
            # Update the content for this item if already present.
            put_node = self.cache[key]
            put_node.content = value
            # set accessed item to head
            self.delete_node(put_node)
            self.add_node_to_head(put_node)
        else:
            # create new node and set it to head
            new_node = DoublyLinkedListNode(key, value)
            self.cache[key] = new_node

            if len(self.cache) <= self.size:
                # if cache not full, add it to head
                self.add_node_to_head(new_node)
            else:
                # if cache is full, remove tail and add it to head
                self.cache.pop(self.tail.prev.cache_key)
                self.delete_node(self.tail.prev)
                self.add_node_to_head(new_node)
        # print("After put({key})".format(key=key))
        # print(self)




