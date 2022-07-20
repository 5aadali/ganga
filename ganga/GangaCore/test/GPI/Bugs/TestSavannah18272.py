

from GangaCore.testlib.GangaUnitTest import GangaUnitTest


class TestSavannah18272(GangaUnitTest):
    def test_Savannah18272(self):
        from GangaCore.GPI import File, Job

        j = Job()
        j.application.exe = File('/hello')
        self.assertEqual(j.application.exe, File('/hello'))
