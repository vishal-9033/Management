from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from user.models import HotelUser


class SuperUserRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
    

class HotelAdminAccessMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class AllAdminMixin(LoginRequiredMixin,UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return True
        elif self.request.user.is_authenticated and self.request.user.is_superuser:
            return True
        else:
            return False

# class CustomerRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
#     def test_func(self):
#         user = HotelUser.objects.get(id=self.kwargs['pk'])
#         print('================================================================')
#         print(user)
#         if user == self.request.user:
#             return True
#         else:
#             return False

# class CustomerRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
#     def test_func(self):
#         if self.request.user.is_authenticated and self.request.user.user_type=="2":
#             return True
#         else:
#             return False