from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Snack


class SnacksTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", email="admin@ltuc.com", password="12345"
        )

        self.snack = Snack.objects.create(
            name="Waffle", purchaser="Dario", description="A batter-based or dough-based cake cooked in a waffle iron patterned to give a characteristic size, shape and surface impression. There are many variations based on the type of iron and recipe used, with over a dozen regional varieties in Belgium alone.",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "Waffle")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.name}", "Waffle")
        self.assertEqual(f"{self.snack.purchaser}", "Dario")
        self.assertEqual(f"{self.snack.description}", "A batter-based or dough-based cake cooked in a waffle iron patterned to give a characteristic size, shape and surface impression. There are many variations based on the type of iron and recipe used, with over a dozen regional varieties in Belgium alone.")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Waffle")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="4"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "purchaser: Dario")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "name": "Waffle",
                "purchaser": "Dario",
                "description": "A batter-based or dough-based cake cooked in a waffle iron patterned to give a characteristic size, shape and surface impression. There are many variations based on the type of iron and recipe used, with over a dozen regional varieties in Belgium alone.",
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="4"))