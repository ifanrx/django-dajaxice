import os
from django.apps import apps
from django.template import Context, Template
from django.test import RequestFactory, TestCase, override_settings

from dajaxice.apps import DajaxiceConfig as DajaxiceAppConfig
from dajaxice.core import DajaxiceConfig, dajaxice_autodiscover, dajaxice_functions
from dajaxice.core.Dajaxice import Dajaxice, DajaxiceFunction, DajaxiceModule
from dajaxice.exceptions import FunctionNotCallableError
from dajaxice.finders import DajaxiceFinder, DajaxiceStorage
from dajaxice.utils import deserialize_form


class DajaxiceModuleTest(TestCase):

    def setUp(self):
        self.module = DajaxiceModule()

    def test_constructor(self):
        self.assertEqual(self.module.functions, {})
        self.assertEqual(self.module.submodules, {})

    def test_add_function(self):
        function = lambda x: x

        self.module.add('test', function)
        self.assertEqual(self.module.functions, {'test': function})
        self.assertEqual(self.module.submodules, {})

        self.module.add('foo.bar', function)
        self.assertEqual(self.module.functions, {'test': function})
        self.assertEqual(list(self.module.submodules.keys()), ['foo'])
        self.assertEqual(self.module.submodules['foo'].functions, {'bar': function})


class DajaxiceFunctionTest(TestCase):

    def test_constructor(self):

        class CalledException(Exception):
            pass

        def callback():
            raise CalledException

        function = DajaxiceFunction(callback, 'foo', 'POST')

        self.assertEqual(function.function, callback)
        self.assertEqual(function.name, 'foo')
        self.assertEqual(function.method, 'POST')
        self.assertRaises(CalledException, function.call)


class DajaxiceTest(TestCase):

    def setUp(self):
        self.dajaxice = Dajaxice()
        self.function = lambda x: x

    def test_constructor(self):
        self.assertEqual(self.dajaxice._registry, {})

    def test_register(self):
        self.dajaxice.register(self.function, 'foo')
        self.assertTrue('foo' in self.dajaxice._registry)
        self.assertEqual(type(self.dajaxice._registry['foo']), DajaxiceFunction)

        def bar_function():
            return

        self.dajaxice.register(bar_function)
        self.assertTrue('dajaxice.tests.bar_function' in self.dajaxice._registry)
        self.assertEqual(type(self.dajaxice._registry['dajaxice.tests.bar_function']), DajaxiceFunction)

    def test__is_callable(self):
        self.dajaxice.register(self.function, 'foo')
        self.dajaxice.register(self.function, 'bar', method='GET')

        self.assertTrue(self.dajaxice.is_callable('foo', 'POST'))
        self.assertTrue(self.dajaxice.is_callable('bar', 'GET'))
        self.assertFalse(self.dajaxice.is_callable('foo', 'GET'))
        self.assertFalse(self.dajaxice.is_callable('bar', 'POST'))
        self.assertFalse(self.dajaxice.is_callable('test', 'POST'))
        self.assertFalse(self.dajaxice.is_callable('test', 'GET'))

    def test_clean_method(self):
        self.assertEqual(self.dajaxice.clean_method('post'), 'POST')
        self.assertEqual(self.dajaxice.clean_method('get'), 'GET')
        self.assertEqual(self.dajaxice.clean_method('POST'), 'POST')
        self.assertEqual(self.dajaxice.clean_method('GET'), 'GET')
        self.assertEqual(self.dajaxice.clean_method('other'), 'POST')

    def test_modules(self):
        self.dajaxice.register(self.function, 'foo')
        self.dajaxice.register(self.function, 'bar')

        self.assertEqual(type(self.dajaxice.modules), DajaxiceModule)
        self.assertEqual(list(self.dajaxice.modules.functions.keys()), ['foo', 'bar'])


class DajaxiceConfigTest(TestCase):

    def setUp(self):
        self.config = DajaxiceConfig()

    def test_defaults(self):
        self.assertFalse(self.config.DAJAXICE_XMLHTTPREQUEST_JS_IMPORT)
        self.assertFalse(self.config.DAJAXICE_JSON2_JS_IMPORT)
        self.assertEqual(self.config.DAJAXICE_EXCEPTION, 'DAJAXICE_EXCEPTION')
        self.assertEqual(self.config.DAJAXICE_MEDIA_PREFIX, 'dajaxice')

        dajaxice_url = r'^%s/' % self.config.DAJAXICE_MEDIA_PREFIX
        self.assertEqual(self.config.dajaxice_url, dajaxice_url)

        self.assertEqual(type(self.config.modules), DajaxiceModule)


class DjangoIntegrationTest(TestCase):

    @override_settings(DEBUG=True)
    def test_calling_not_registered_function(self):
        self.assertRaises(FunctionNotCallableError, self.client.post, '/dajaxice/dajaxice.tests.this_function_not_exist/')

    def test_calling_registered_function(self):
        response = self.client.post('/dajaxice/dajaxice.tests.test_foo/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '{"foo": "bar"}')

    def test_calling_registered_function_with_params(self):

        response = self.client.post('/dajaxice/dajaxice.tests.test_foo_with_params/', {'argv': '{"param1":"value1"}'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '{"param1": "value1"}')

    def test_bad_function(self):

        response = self.client.post('/dajaxice/dajaxice.tests.test_ajax_exception/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), "DAJAXICE_EXCEPTION")

    def test_get_register(self):

        response = self.client.get('/dajaxice/dajaxice.tests.test_get_register/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '{"foo": "user"}')

    def test_get_custom_name_register(self):

        response = self.client.get('/dajaxice/get_user_data/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '{"bar": "user"}')

    def test_multi_register(self):

        response = self.client.get('/dajaxice/get_multi/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '{"foo": "multi"}')

        response = self.client.post('/dajaxice/post_multi/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '{"foo": "multi"}')


class DajaxiceFinderTest(TestCase):

    def setUp(self):
        self.finder = DajaxiceFinder()

    def test_find_core_js(self):
        match = self.finder.find('dajaxice/dajaxice.core.js')
        self.assertTrue(bool(match))
        self.assertTrue(os.path.exists(match))
        with open(match, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('var Dajaxice =', content)
        self.assertIn('dajaxice_endpoint', content)

    def test_find_non_existent(self):
        match = self.finder.find('nonexistent/file.js')
        self.assertEqual(match, [])

    def test_storage_exists_and_listdir(self):
        storage = DajaxiceStorage()
        self.assertTrue(storage.exists('dajaxice/dajaxice.core.js'))
        self.assertFalse(storage.exists('random.js'))
        folders, files = storage.listdir('dajaxice')
        self.assertIn('dajaxice.core.js', files)


class DajaxiceTemplateTagTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_dajaxice_js_import_with_request(self):
        request = self.factory.get('/')
        template = Template('{% load dajaxice_templatetags %}{% dajaxice_js_import %}')
        rendered = template.render(Context({'request': request}))
        self.assertIn("var dajaxice_endpoint = '/dajaxice/'", rendered)
        self.assertIn('<script src="/static/dajaxice/dajaxice.core.js"', rendered)

    def test_dajaxice_js_import_nocsrf(self):
        template = Template("{% load dajaxice_templatetags %}{% dajaxice_js_import 'nocsrf' %}")
        rendered = template.render(Context({}))
        self.assertIn("var dajaxice_endpoint = '/dajaxice/'", rendered)
        self.assertIn('<script src="/static/dajaxice/dajaxice.core.js"', rendered)


class DajaxiceUtilsTest(TestCase):

    def test_deserialize_form(self):
        form_data = deserialize_form('name=Antigravity&task=DjangoUpgrade&number=42')
        self.assertEqual(form_data.get('name'), 'Antigravity')
        self.assertEqual(form_data.get('task'), 'DjangoUpgrade')
        self.assertEqual(form_data.get('number'), '42')


class DajaxiceAppConfigTest(TestCase):

    def test_app_config(self):
        config = apps.get_app_config('dajaxice')
        self.assertIsInstance(config, DajaxiceAppConfig)
        self.assertEqual(config.name, 'dajaxice')
        self.assertEqual(config.verbose_name, 'Dajaxice')


class DajaxiceAutodiscoverTest(TestCase):

    def test_autodiscover_idempotent(self):
        # Initial count
        count_before = len(dajaxice_functions._registry)
        self.assertGreater(count_before, 0)
        # Calling autodiscover again must be safe and idempotent
        dajaxice_autodiscover()
        self.assertEqual(len(dajaxice_functions._registry), count_before)
