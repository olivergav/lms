from django.contrib.auth.models import Permission, Group
from django.urls import reverse


def test_view_create_course_anonymous_user(client):
	url = reverse('courses:create-course')
	response = client.get(url)
	assert response.status_code == 403


def test_view_create_course_logged_in_user(client, user):
	# permission = Permission.objects.get(name='Can add course')
	# user.user_permissions.add(permission)

	group = Group.objects.get(name='instructors')

	user.groups.add(group['name'])
	client.force_login(user)
	url = reverse('courses:create-course')
	response = client.get(url)

	print('*' * 50)
	# print(permission)
	# print(group['name'])
	print(user.user_permissions)
	print('*' * 50)

	assert response.status_code == 200
	assert 'Add new course' in response.content.decode('UTF-8')
