from django.urls import path
from chirps.views import ChirpListCreateView, ChirpRetrieveUpdateDeleteView, ChirpCommentCreateView, ChirpLikeView

urlpatterns = [
     path("chirp_list_create/", ChirpListCreateView.as_view(), name="chirp_list_create"),
     path("chirp_retrieve_update_delete/<slug:pk>/", ChirpRetrieveUpdateDeleteView.as_view(), name="chirp_retrieve_update_delete"),
     path("<chirp_id>/like/", ChirpLikeView.as_view(), name="chirp_like"),
     path("<chirp_id>/comment/", ChirpCommentCreateView.as_view(), name="chirp_comment"),
]