""" Implements a simple priority queue using a binary heap, supports push, extract min and update operations 
    The root of the heap is the minimum element, i.e., the element with the highest priority (lowest priority value) """
class PQ:
    def __init__(self):
        ## item conatains the mapping from key to index
        self.items = {}
        ## heap contains pairs of (priority, key)
        self.heap = []
    
    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self.heap)
    
    def __bool__(self):
        """Return True if the priority queue is not empty."""
        return len(self.heap) > 0
    
    def push(self, key, priority):
        self.items[key] = len(self.heap)
        self.heap.append((priority, key))
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            raise IndexError("extract_min from empty priority queue")
        min_item = self.heap[0]
        last_item = self.heap.pop()
        del self.items[min_item[1]]
        if self.heap:
            self.heap[0] = last_item
            self.items[last_item[1]] = 0
            self._heapify_down(0)
        return min_item[1], min_item[0]
    
    def update(self, key, new_priority):
        index = self.items.get(key)
        if index is None:
            raise KeyError("Key not found in priority queue")
        old_priority, _ = self.heap[index]
        self.heap[index] = (new_priority, key)
        if new_priority < old_priority:
            self._heapify_up(index)
        else:
            self._heapify_down(index)

    def _heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index][0] < self.heap[parent_index][0]:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                self.items[self.heap[index][1]] = index
                self.items[self.heap[parent_index][1]] = parent_index
                index = parent_index
            else:
                break
    
    """ heapify down from index is called when the root is replaced with an element that is larger than its children """
    def _heapify_down(self, index):
        size = len(self.heap)
        while True:
            smallest = index
            left = 2 * index + 1
            right = 2 * index + 2
            if left < size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                self.items[self.heap[index][1]] = index
                self.items[self.heap[smallest][1]] = smallest
                index = smallest
            else:
                break
