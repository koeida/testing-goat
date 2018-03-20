from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item, List

class ListAndItemModelTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='i1', list=list_)
        Item.objects.create(text='i2', list=list_)
        
        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'i1')
        self.assertContains(response, 'i2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        txt = 'A new list item'
        response = self.client.post(
            '/lists/new', 
            data={'item_text': txt})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, txt)

    def test_redirect_after_post(self):
        response = self.client.post(
            '/lists/new', 
            data={'item_text': 'lala'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
