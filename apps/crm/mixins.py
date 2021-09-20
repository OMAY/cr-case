from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class StaffAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an staff."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_manager:
            return redirect("crm:home")
        return super().dispatch(request, *args, **kwargs)





class RedirectToPreviousMixin:

    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']




#
# cyrillic_letters = {
#         u'а': u'a',
#         u'б': u'b',
#         u'в': u'v',
#         u'г': u'g',
#         u'д': u'd',
#         u'е': u'e',
#         u'ё': u'e',
#         u'ж': u'zh',
#         u'з': u'z',
#         u'и': u'i',
#         u'й': u'y',
#         u'к': u'k',
#         u'л': u'l',
#         u'м': u'm',
#         u'н': u'n',
#         u'о': u'o',
#         u'п': u'p',
#         u'р': u'r',
#         u'с': u's',
#         u'т': u't',
#         u'у': u'u',
#         u'ф': u'f',
#         u'х': u'h',
#         u'ц': u'ts',
#         u'ч': u'ch',
#         u'ш': u'sh',
#         u'щ': u'sch',
#         u'ъ': u'',
#         u'ы': u'y',
#         u'ь': u'',
#         u'э': u'e',
#         u'ю': u'yu',
#         u'я': u'ya'
#     }
#
#
# def from_cyrillic_to_eng(text: str):
#     text = text.replace(' ', '_').lower()
#     tmp = ''
#     for ch in text:
#         tmp += cyrillic_letters.get(ch, ch)
#     return tmp
