from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('login/', views.login_receiver, name='login_receiver'),
    path('logout/', views.logout_receiver, name='logout_receiver'),
    path('course/', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/edit/<int:course_id>/', views.course_edit, name='course_detail_edit'),
    path('course/edit_submit/', views.course_edit_submit, name='course_edit_submit'),
    path('course/comments_submit/', views.course_comments_submit, name='course_comments_submit'),
    path('course/delete/<int:course_id>/', views.delete_course, name='course_delete'),
    path('signup/', views.signup_invite, name='signup_invite'),
    path('signup/check/', views.signup_check, name='signup_receiver'),
    path('tools/', views.admin_tools, name='admin_tools'),
    path('tools/invitation/', views.invitation_code, name='invitation_code'),
    path('tools/invitation/invalid/<int:code_id>', views.invitation_code_invalid, name='invitation_code_invalid'),
    path('tools/comments/', views.view_comment, name='view_comment'),
    path('tools/comments/<int:user_id>', views.view_your_comment, name='view_your_comment'),
    path('account/', views.account_info_view, name='account_info_view'),
    path('account/<int:user_id>', views.user_info_view, name='user_info_view'),
    path('account/edit/', views.account_info_edit, name='account_info_edit'),
    path('account/edit_submit/', views.account_info_submit, name='account_info_submit'),
    path('account/password/', views.account_password_edit, name='account_password_edit'),
    path('account/password/submit/', views.account_password_submit, name='account_password_submit'),
    path('comments/<int:comment_id>/', views.comment_operation, name='comment_operation'),
    path('validate/email/', views.validate_email, name='validate_email'),
    path('validate/username/', views.validate_user, name='validate_user'),
    path('validate/invitationcode/', views.validate_invitationcode, name='validate_invitationcode'),
    path('vote/course/<int:course_id>', views.vote_course, name='vote_course'),
]
