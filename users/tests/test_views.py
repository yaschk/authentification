from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse


class UserLoginViewTest(TestCase):

    def test_login_view_url_exists_at_desired_location(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

    def test_login_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

    def test_login_view_uses_correct_template(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/login.html')


class UserLogoutViewTest(TestCase):

    def test_logout_view_url_exists_at_desired_location(self):
        resp = self.client.get('/logout/')
        self.assertEqual(resp.status_code, 200)

    def test_logout_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 200)

    def test_logout_view_uses_correct_template(self):
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/logged_out.html')


class UserSignupViewTest(TestCase):

    def test_signup_view_url_exists_at_desired_location(self):
        resp = self.client.get('/signup/')
        self.assertEqual(resp.status_code, 200)

    def test_signup_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('signup'))
        self.assertEqual(resp.status_code, 200)

    def test_signup_view_uses_correct_template(self):
        resp = self.client.get(reverse('signup'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/signup.html')


class UserResetPasswordViewTest(TestCase):

    def test_reset_password_view_url_exists_at_desired_location(self):
        resp = self.client.get('/password-reset/')
        self.assertEqual(resp.status_code, 200)

    def test_reset_password_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('password_reset'))
        self.assertEqual(resp.status_code, 200)

    def test_reset_password_view_uses_correct_template(self):
        resp = self.client.get(reverse('password_reset'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/password_reset_form.html')


class UserResetPasswordUsernameDoneViewTest(TestCase):

    def test_reset_password_username_view_url_exists_at_desired_location(self):
        resp = self.client.get('/password-reset/username/done/')
        self.assertEqual(resp.status_code, 200)

    def test_reset_password_username_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('password_reset_user'))
        self.assertEqual(resp.status_code, 200)

    def test_reset_password_username_view_uses_correct_template(self):
        resp = self.client.get(reverse('password_reset_user'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/password_reset_user_done.html')


class UserResetPasswordEmailDoneViewTest(TestCase):

    def test_reset_password_email_view_url_exists_at_desired_location(self):
        resp = self.client.get('/password-reset/email/done/')
        self.assertEqual(resp.status_code, 200)

    def test_reset_password_email_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('password_reset_email'))
        self.assertEqual(resp.status_code, 200)

    def test_reset_password_email_view_uses_correct_template(self):
        resp = self.client.get(reverse('password_reset_email'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/password_reset_user_done.html')


class UserResetPasswordPhoneDoneViewTest(TestCase):

    def test_reset_password_phone_view_url_exists_at_desired_location(self):
        resp = self.client.get('/password-reset/phone/done/')
        self.assertEqual(resp.status_code, 200)

    def test_reset_password_phone_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('password_reset_phone'))
        self.assertEqual(resp.status_code, 200)

    def test_reset_password_phone_view_uses_correct_template(self):
        resp = self.client.get(reverse('password_reset_phone'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/password_reset_phone_done.html')


class UserResetPasswordDoneViewTest(TestCase):

    def test_reset_done_view_url_exists_at_desired_location(self):
        resp = self.client.get('/reset/done/')
        self.assertEqual(resp.status_code, 200)

    def test_reset_done_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(resp.status_code, 200)

    def test_reset_done_view_uses_correct_template(self):
        resp = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/password_reset_complete.html')


class UserAccessBannedViewTest(TestCase):

    def test_access_banned_view_url_exists_at_desired_location(self):
        resp = self.client.get('/login/banned/')
        self.assertEqual(resp.status_code, 200)

    def test_access_banned_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('banned'))
        self.assertEqual(resp.status_code, 200)

    def test_access_banned_view_uses_correct_template(self):
        resp = self.client.get(reverse('banned'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/banned.html')


class UserActivationSendViewTest(TestCase):

    def test_activation_sent_view_url_exists_at_desired_location(self):
        resp = self.client.get('/account-activation-sent/')
        self.assertEqual(resp.status_code, 200)

    def test_activation_sent_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('account_activation_sent'))
        self.assertEqual(resp.status_code, 200)

    def test_activation_sent_view_uses_correct_template(self):
        resp = self.client.get(reverse('account_activation_sent'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/account_activation_sent.html')


class UserVerificationTokenViewTest(TestCase):

    def test_ver_token_view_url_exists_at_desired_location(self):
        resp = self.client.get('/verification/token/')
        self.assertEqual(resp.status_code, 200)

    def test_ver_token_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('token_validation'))
        self.assertEqual(resp.status_code, 200)

    def test_ver_token_view_uses_correct_template(self):
        resp = self.client.get(reverse('token_validation'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'registration/token_validation.html')


class UserQuestionResetViewTest(TestCase):

    def setUp(self):
        test_user1 = CustomUser.objects.create_user(username='testuser1', password='12345')
        # test_user1.email = 'test@i.ua'
        test_user1.save()

    def test_user_exist_view_url_exists_at_desired_location(self):
        resp = self.client.get('/password-reset/testuser1/')
        self.assertEqual(resp.status_code, 200)

    def test_user_not_exist_view_url_exists_at_desired_location(self):
        resp = self.client.get('/password-reset/testuser100/')
        self.assertEqual(resp.status_code, 302)


class UserIndexPageViewTest(TestCase):

    def setUp(self):
        test_user1 = CustomUser.objects.create_user(username='testuser1', password='12345')
        # test_user1.email = 'test@i.ua'
        test_user1.save()

    def test_index_view_url_exists_at_desired_location(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_ver_token_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_ver_token_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'landing/home.html')


