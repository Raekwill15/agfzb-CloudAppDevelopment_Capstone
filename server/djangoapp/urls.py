from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='about/', view=views.about, name='about'),
    # path for contact us view
    path(route='contact/', view=views.contact, name='contact'),

    # path for registration
    path(route='signup/', view=views.registration_request, name='signup'),
    # path for login
    path(route="login/", view=views.login_request, name='login'),

    # path for logout
    path(route="logout/", view=views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    path(route='dealerid/<int:id>/', view=views.get_dealer_details, name='dealerbyid'),

    path(route='state/<str:state>/', view=views.get_dealers_by_state, name="dealersbystate"),

    # path for dealer reviews view

    path(route='review/<int:id>/', view=views.get_dealer_details, name="reviewsbyid"),

    # path for add a review view

    path(route='review/add/<int:dealer_id>/', view=views.add_review, name='add_review')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)