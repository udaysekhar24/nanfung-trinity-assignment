import pytest
from assignment4 import LRUCache


class TestLRUCache:

    def test_get_fail1(self):
        # fail scenario: search for item not added in cache.
        lru = LRUCache.LRUCache(2)
        lru.put(1, "A")
        lru.put(2, "B")
        lru.get(1)
        lru.put(3, "C")
        lru.put(1, "D")
        lru.get(2)
        content = lru.get(5)
        assert content is None

    def test_get_fail2(self):
        # fail scenario: search for item added previously in cache but removed due to max size.
        lru = LRUCache.LRUCache(2)
        lru.put(1, "A")
        lru.put(2, "B")
        lru.get(1)
        lru.put(3, "C")
        lru.put(1, "D")
        lru.get(2)
        content = lru.get(2)
        assert content is None

    def test_get_fail3(self):
        # fail scenario: search for item in empty cache.
        lru = LRUCache.LRUCache(0)
        content = lru.get(2)
        assert content is None

    def test_get_success1(self):
        # success scenario: search for item added previously in cache.
        lru = LRUCache.LRUCache(2)
        lru.put(1, "A")
        lru.put(2, "B")
        lru.get(1)
        lru.put(3, "C")
        lru.put(1, "D")
        lru.get(2)
        content = lru.get(3)
        assert content == "C"

    def test_get_success2(self):
        # success scenario: search for item added previously in cache and updated.
        lru = LRUCache.LRUCache(2)
        lru.put(1, "A")
        lru.put(2, "B")
        lru.get(1)
        lru.put(3, "C")
        lru.put(1, "D")
        lru.get(2)
        content = lru.get(1)
        assert content == "D"

    def test_get_success3(self):
        # success scenario: check for head in DLL
        lru = LRUCache.LRUCache(2)
        lru.put(1, "A")
        lru.put(2, "B")
        lru.get(1)
        lru.put(3, "C")
        lru.put(1, "D")
        lru.get(2)
        content = lru.get(1)
        assert content == "D"

    def test_get_success5(self):
        # success scenario: check for tail in DLL
        lru = LRUCache.LRUCache(2)
        lru.put(1, "A")
        lru.put(2, "B")
        lru.get(1)
        lru.put(3, "C")
        lru.put(1, "D")
        lru.get(2)
        content = lru.tail.prev.content
        assert content == "C"


if __name__ == '__main__':
    pytest.main()
