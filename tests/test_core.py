import os
import unittest

from simple_relative_path import relative_path


class RelativePathTests(unittest.TestCase):
    def test_same_directory(self):
        self.assertEqual(relative_path("/a/b", "/a/b"), ".")

    def test_child_directory(self):
        self.assertEqual(relative_path("/a", "/a/b"), "b")

    def test_parent_directory(self):
        self.assertEqual(relative_path("/a/b", "/a"), "..")

    def test_sibling_directories(self):
        self.assertEqual(relative_path("/a/b", "/a/c"), "../c")

    def test_deep_common_prefix(self):
        self.assertEqual(relative_path("/a/b/c/d", "/a/b/e/f"), "../../e/f")

    def test_trailing_separators_are_normalised(self):
        self.assertEqual(relative_path("/a/b/", "/a/c/"), "../c")

    def test_different_roots_return_target(self):
        # On POSIX there is no drive letter, so this is the absolute/relative case.
        self.assertEqual(relative_path("/a", "b"), "b")

    def test_relative_start_and_absolute_target(self):
        self.assertEqual(relative_path("a", "/b"), "/b")

    def test_relative_to_relative(self):
        self.assertEqual(relative_path("a/b", "a/c"), "../c")

    def test_dot_components_are_normalised(self):
        self.assertEqual(relative_path("/a/./b", "/a/b/c"), "c")

    def test_parent_components_are_normalised(self):
        self.assertEqual(relative_path("/a/b/..", "/a/c"), "c")

    def test_custom_separator(self):
        self.assertEqual(relative_path("/a/b", "/a/c", sep="/"), "../c")

    def test_windows_style_drive_mismatch(self):
        if os.name != "nt":
            self.skipTest("drive-letter behaviour is only meaningful on Windows")
        self.assertEqual(relative_path("C:\\a", "D:\\b"), "D:\\b")


if __name__ == "__main__":
    unittest.main()
