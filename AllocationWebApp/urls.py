from django.urls import path
from AllocationWebApp import views
from django.contrib.auth.views import LogoutView

app_name = 'AllocationWebApp'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='AllocationWebApp:login'), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.ProjectList.as_view(), name='projects'),
    path('my-projects', views.SupervisorProjectList.as_view(), name='supervisor-projects'),
    path('project/<int:pk>/', views.ProjectView.as_view(), name='project'),
    path('my-project/<int:pk>/', views.SupervisorProjectView.as_view(), name='supervisor-project'),
    path('allocation-project/<int:pk>/', views.StudentAllocationProjectView.as_view(), name='student-allocation'),
    path('preference-project/<int:pk>/', views.PreferenceProjectView.as_view(), name='preference-project'),
    path('project-create/', views.ProjectCreate.as_view(), name='project-create'),
    path('supervisor-project-create/', views.SupervisorProjectCreate.as_view(), name='supervisor-project-create'),
    path('project-edit/<int:pk>/', views.ProjectEdit.as_view(), name='project-edit'),
    path('my-project-edit/<int:pk>/', views.SupervisorProjectEdit.as_view(), name='supervisor-project-edit'),
    path('project-delete/<int:pk>/', views.ProjectDelete.as_view(), name='project-delete'),
    path('my-project-delete/<int:pk>/', views.SupervisorProjectDelete.as_view(), name='supervisor-project-delete'),
    path('favourite-post/<int:id>/', views.favourite_post, name='favourite-post'),
    path('user-delete/<int:pk>/', views.UserDelete.as_view(), name='user-delete'),
    path('preferences/', views.preferences_list, name='preferences'),
    path('students/', views.StudentList.as_view(), name='students'),
    path('student/<int:pk>/', views.StudentView.as_view(), name='student-view'),
    path('admin-panel/', views.admin_panel, name='admin-panel'),
    path('stage-control/', views.stage_control, name='stage-control'),
    path('algorithms/', views.algorithms, name='algorithms'),
    path('algorithms-complete/', views.cmd_line, name="alg-cmd-line"),
    # path('algorithms-populate/', views.populate_test, name="populate-test"),
    path('upload-csv/', views.upload_csv, name='csv-upload'),
    path('allocation/', views.student_allocation, name='student-allocation'),
    path('my-allocations/', views.supervisor_allocations, name='supervisor-allocations'),
]