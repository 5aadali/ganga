import time
from GangaCore.testlib.GangaUnitTest import GangaUnitTest

master_timeout = 300.

def dummySleep(someJob):
    my_timeout = 0.
    while someJob.status not in ['completed', 'failed', 'killed', 'removed'] and my_timeout < master_timeout:
        time.sleep(1.)
        my_timeout += 1.

class TestMonitoring(GangaUnitTest):

    def setUp(self):
        """Make sure that the Job object isn't destroyed between tests"""
        extra_opts = [('PollThread', 'autostart', 'False'), ('PollThread', 'base_poll_rate', 1)]
        super(TestMonitoring, self).setUp(extra_opts=extra_opts)

    def tearDown(self):
        from GangaCore.Utility.Config import getConfig
        super(TestMonitoring, self).tearDown()

    def test_a_JobConstruction(self):
        from GangaCore.GPI import Job, jobs, disableMonitoring

        j = Job()

        self.assertEqual(len(jobs), 1)

        j.submit()

        self.assertNotEqual(j.status, 'new')

    def test_b_EnableMonitoring(self):
        from GangaCore.GPI import enableMonitoring, Job, jobs

        enableMonitoring()

        j = Job()
        j.submit()

        dummySleep(j)

        self.assertNotEqual(jobs(0).status, 'submitted')

    def test_c_disableMonitoring(self):
        from GangaCore.GPI import disableMonitoring

        disableMonitoring()

    def test_d_anotherNewJob(self):
        from GangaCore.GPI import Job, jobs

        j = Job()
        j.submit()

        self.assertNotEqual(j.status, 'new')

    def test_e_reEnableMon(self):
        from GangaCore.GPI import disableMonitoring, enableMonitoring, Job, jobs

        disableMonitoring()
        enableMonitoring()
        disableMonitoring()
        enableMonitoring()

        j = Job()
        j.submit()

        dummySleep(j)

        self.assertEqual(j.status, 'completed')

    def test_f_reallyDisabled(self):
        from GangaCore.GPI import disableMonitoring, enableMonitoring, Job

        disableMonitoring()
        j = Job()
        j.submit()

        self.assertEqual(j.status, 'submitted')

        enableMonitoring()

        dummySleep(j)

        self.assertEqual(j.status, 'completed')

    # NEW TESTS BASED ON MODIFIED runMonitoring FUNCTION

    def test_g_runMonitoring_with_int(self):
        """Test runMonitoring with a single job index (int)"""
        from GangaCore.GPI import runMonitoring, Job, jobs

        j = Job()
        j.submit()
        dummySleep(j)

        result = runMonitoring(jobs=0, steps=1)
        self.assertTrue(result)

    def test_h_runMonitoring_with_list_of_int(self):
        """Test runMonitoring with a list of job indices (list of ints)"""
        from GangaCore.GPI import runMonitoring, Job, jobs

        j1 = Job()
        j2 = Job()
        j1.submit()
        j2.submit()
        dummySleep(j1)
        dummySleep(j2)

        result = runMonitoring(jobs=[0, 1], steps=1)
        self.assertTrue(result)

    def test_i_runMonitoring_with_job_object(self):
        """Test runMonitoring with a job object"""
        from GangaCore.GPI import runMonitoring, Job

        j = Job()
        j.submit()
        dummySleep(j)

        result = runMonitoring(jobs=j, steps=1)
        self.assertTrue(result)

