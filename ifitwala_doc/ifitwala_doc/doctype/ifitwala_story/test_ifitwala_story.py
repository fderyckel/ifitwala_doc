from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase

from ifitwala_doc.api import site as site_api


def _unique(prefix: str) -> str:
    return f"{prefix}-{frappe.generate_hash(length=8).lower()}"


class TestIfitwalaStory(FrappeTestCase):
    def test_published_story_sets_slug_publish_date_and_read_time(self):
        with patch('frappe.enqueue'):
            story = frappe.get_doc(
                {
                    'doctype': 'Ifitwala Story',
                    'title': 'Platform clarity for school leaders',
                    'status': 'Published',
                    'story_type': "What's New",
                    'summary': 'A sharper editorial summary.',
                    'body_md': '# Headline\n\nThis story explains why the update matters for institutions.',
                    'author_name': 'Ifitwala Team',
                    'cover_image': '/files/insights-cover.png',
                }
            ).insert()

        self.assertEqual(story.slug, 'platform-clarity-for-school-leaders')
        self.assertTrue(story.published_on)
        self.assertGreaterEqual(story.estimated_read_minutes, 1)
        self.assertEqual(story.cover_image_alt, story.title)

    def test_requires_complete_cta_pairs(self):
        with self.assertRaises(frappe.ValidationError):
            with patch('frappe.enqueue'):
                frappe.get_doc(
                    {
                        'doctype': 'Ifitwala Story',
                        'title': _unique('Incomplete CTA'),
                        'status': 'Draft',
                        'story_type': 'Product Insight',
                        'body_md': 'Body copy',
                        'primary_cta_label': 'Book a Demo',
                    }
                ).insert()

    def test_story_endpoints_return_topics_and_related_content(self):
        with patch('frappe.enqueue'):
            first = frappe.get_doc(
                {
                    'doctype': 'Ifitwala Story',
                    'title': _unique('Admissions visibility'),
                    'status': 'Published',
                    'story_type': 'School Operations',
                    'topic': 'Admissions',
                    'featured': 1,
                    'featured_priority': 1,
                    'summary': 'Operational story summary.',
                    'body_md': 'This published story focuses on admissions workflows.',
                    'author_name': 'Editorial Team',
                    'key_takeaways': [
                        {'title': 'Leadership visibility', 'detail': 'Admissions teams get cleaner pipeline oversight.'},
                    ],
                }
            ).insert()
            second = frappe.get_doc(
                {
                    'doctype': 'Ifitwala Story',
                    'title': _unique('Admissions onboarding'),
                    'status': 'Published',
                    'story_type': 'School Operations',
                    'topic': 'Admissions',
                    'summary': 'Another story in the same topic.',
                    'body_md': 'This story focuses on onboarding after admissions.',
                    'author_name': 'Editorial Team',
                }
            ).insert()

        stories = site_api.list_stories()
        story_slugs = {item['slug'] for item in stories}
        self.assertIn(first.slug, story_slugs)
        self.assertIn(second.slug, story_slugs)

        record = site_api.get_story(first.slug)
        self.assertEqual(record['slug'], first.slug)
        self.assertEqual(record['key_takeaways'][0]['title'], 'Leadership visibility')
        self.assertTrue(any(item['slug'] == second.slug for item in record['related_stories']))

        topics = site_api.get_story_topics()
        admissions = next((row for row in topics if row['topic'] == 'Admissions'), None)
        self.assertIsNotNone(admissions)
        self.assertEqual(admissions['count'], 2)
