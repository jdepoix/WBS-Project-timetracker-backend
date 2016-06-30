from django.test.runner import DiscoverRunner


class UnmanagedModelTestRunner(DiscoverRunner):
    '''
    Test runner that automatically makes all unmanaged models in your Django project managed for the duration of the
    test run.
    '''
    def setup_test_environment(self, *args, **kwargs):
        from django.apps import apps

        self.unmanaged_models = [m for m in apps.get_models() if not m._meta.managed]

        for m in self.unmanaged_models:
            m._meta.managed = True

        super(UnmanagedModelTestRunner, self).setup_test_environment(**kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(UnmanagedModelTestRunner, self).teardown_test_environment(**kwargs)

        for m in self.unmanaged_models:
            m._meta.managed = False
