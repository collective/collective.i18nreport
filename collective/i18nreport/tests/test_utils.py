from collective.i18nreport import utils
from collective.i18nreport.tests.helpers import make_absolute
from collective.i18nreport.tests.helpers import make_relative
from collective.i18nreport.tests.helpers import make_relative_recursively
from unittest2 import TestCase
import os


TEST_EXAMPLE_PATH = os.path.join(os.path.dirname(__file__), 'example')


class TestDetectDomains(TestCase):

    def test_find_domains_in_path(self):
        self.maxDiff = None
        self.assertEqual(
            make_relative_recursively(utils.find_domains_in_path(TEST_EXAMPLE_PATH)),

            {'foo/i18n/plone.pot': {
                    'domain': 'plone',
                    'languages':{
                        'nl': 'foo/i18n/plone-nl.po'}},

             'foo/locales/locales/linguaplone.pot': {
                    'domain': 'linguaplone',
                    'languages': {
                        'nl': 'foo/locales/locales/nl/LC_MESSAGES/linguaplone.po'}},

             'foo/locales/locales/plone.pot': {
                    'domain': 'plone',
                    'languages': {
                        'nl': 'foo/locales/locales/nl/LC_MESSAGES/plone.po'}},

             })

    def test_find_files_in_path(self):
        results = map(make_relative, utils.find_files_in_path('pot', TEST_EXAMPLE_PATH))

        self.assertEquals(results, ['foo/i18n/plone.pot',
                                    'foo/locales/locales/linguaplone.pot',
                                    'foo/locales/locales/plone.pot'])

    def test_get_domain_of_potfile(self):
        self.assertEqual(
            utils.get_domain_of_potfile(make_absolute('foo/i18n/plone.pot')),
            'plone')

        self.assertEqual(
            utils.get_domain_of_potfile(make_absolute('foo/locales/locales/linguaplone.pot')),
            'linguaplone')

        self.assertEqual(
            utils.get_domain_of_potfile(make_absolute('foo/locales/locales/plone.pot')),
            'plone')

    def test_get_language_of_pofile(self):
        self.assertEqual(utils.get_language_of_pofile(
                make_absolute('foo/locales/locales/nl/LC_MESSAGES/linguaplone.po')),
                'nl')

        self.assertEqual(utils.get_language_of_pofile(
                    make_absolute('foo/locales/locales/nl/LC_MESSAGES/plone.po')),
                    'nl')

        self.assertEqual(utils.get_language_of_pofile(make_absolute('foo/i18n/plone-nl.po')),
                         'nl')

    def test_get_definition_type(self):
        self.assertEqual(utils.get_definition_type('foo/i18n/plone.pot'), 'i18n')
        self.assertEqual(utils.get_definition_type('foo/locales/locales/plone.pot'), 'locales')

        with self.assertRaises(ValueError):
            utils.get_definition_type('foo')

    def test_get_pofiles_for_potfile__i18n(self):
        result = utils.get_pofiles_for_potfile(make_absolute('foo/i18n/plone.pot'))
        result = make_relative_recursively(result)

        self.assertEqual(result, {'nl': 'foo/i18n/plone-nl.po'})

    def test_get_pofiles_for_potfile__locales(self):
        result = utils.get_pofiles_for_potfile(make_absolute('foo/locales/locales/plone.pot'))
        result = make_relative_recursively(result)

        self.assertEqual(result, {'nl': 'foo/locales/locales/nl/LC_MESSAGES/plone.po'})
