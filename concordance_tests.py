import unittest
from concordance import *
from hash_quad import *


class TestList(unittest.TestCase):



    def test_03(self) -> None:
        conc = Concordance()
        conc.load_stop_table("stop_words.txt")
        conc.load_concordance_table("war_and_peace.txt")
        conc.write_concordance("war_and_peace_concordance.txt")
        self.assertTrue(compare_files("declaration_con.txt", "declaration_sol.txt"))

    def test_error(self) -> None:
        conc = Concordance()
        with self.assertRaises(FileNotFoundError):
            conc.load_stop_table('afsjkdhfoukash.txt')
            conc.load_concordance_table('asdjhfkjashdfkjshad.txt')


# Compare files - takes care of CR/LF, LF issues
def compare_files(file1: str, file2: str) -> bool:
    match = True
    done = False
    with open(file1, "r") as f1:
        with open(file2, "r") as f2:
            while not done:
                line1 = f1.readline().strip()
                line2 = f2.readline().strip()
                if line1 == '' and line2 == '':
                    done = True
                if line1 != line2:  # pragma: no cover
                    done = True
                    match = False
    return match


if __name__ == '__main__':
    unittest.main(warnings="ignore")
