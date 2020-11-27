# -*- coding: utf-8 -*-

from .utils import gen_word_variants


class SlicedWordSet:
    def __init__(self, char_map, slice_len):
        self._base = {}
        self._char_map = char_map
        self._slice_len = slice_len

    def add_word(self, word):
        """
        Adds a word to the set.

        Args:
            word (str): Word to add to the set.

        Raises:
            TypeError: if `word` is not a str.
            ValueError: if `word` is empty.
        """
        if not isinstance(word, str):
            raise TypeError("word must be a str")
        if not word:
            raise ValueError("word must be non-empty")
        if word in self:
            return
        slices = self._get_slices(word)

        # Find place in the tree to start inserting unique nodes.
        parent_dict = self._base
        is_subset = True
        for parent_slice_i, s in enumerate(slices):
            if s in parent_dict:
                if parent_dict[s] is None:
                    new_dict = {"": None}
                    for var in gen_word_variants(self._char_map, s):
                        parent_dict[var] = new_dict
                parent_dict = parent_dict[s]
            else:
                is_subset = False
                break

        if is_subset:
            parent_dict[""] = None
            return

        # Create nodes from the bottom-up (child-most first).
        child_dict = None
        for s in reversed(slices[parent_slice_i + 1 :]):
            new_dict = {}
            for var in gen_word_variants(self._char_map, s):
                new_dict[var] = child_dict
            child_dict = new_dict
        for var in gen_word_variants(self._char_map, slices[parent_slice_i]):
            parent_dict[var] = child_dict

    def _get_slices(self, word):
        """Returns string slices on increments of `self._slice_len`"""
        slices = []
        remain = word
        while remain:
            slices.append(remain[: self._slice_len])
            remain = remain[self._slice_len :]
        return slices

    def __contains__(self, key):
        if not isinstance(key, str):
            raise TypeError("key must be a str")
        if not key:
            raise ValueError("key must be non-empty")

        first_slice = key[: self._slice_len]
        if first_slice not in self._base:
            return False

        remain = key
        cur_dict = self._base
        while True:
            cur_slice = remain[: self._slice_len]
            if cur_slice not in cur_dict:
                return False
            if len(cur_slice) < self._slice_len:
                return True

            cur_dict = cur_dict[cur_slice]
            remain = remain[self._slice_len :]
            if cur_dict is None:
                return remain == ""
            if not remain:
                return "" in cur_dict
