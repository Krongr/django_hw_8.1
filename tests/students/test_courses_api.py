import pytest

from students.models import Course

@pytest.mark.django_db
def test_get_specific_course(api_client, course_factory):
    courses = course_factory(_quantity=1)

    response = api_client.get(f'/api/v1/courses/{courses[0].id}/')

    assert response.status_code == 200
    assert response.json()['id'] == courses[0].id

@pytest.mark.django_db
def test_get_courses_list(api_client, course_factory):
    courses = course_factory(_quantity=20)

    response = api_client.get('/api/v1/courses/')

    assert response.status_code == 200
    assert len(response.json()) == len(courses)
    for i, resp in enumerate(response.json()):
        assert resp['id'] == courses[i].id

@pytest.mark.django_db
def test_get_course_filtered_by_id(api_client, course_factory):
    courses = course_factory(_quantity=20)

    response = api_client.get(f'/api/v1/courses/?id={courses[10].id}')

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == courses[10].id

@pytest.mark.django_db
def test_get_course_filtered_by_name(api_client, course_factory):
    courses = course_factory(_quantity=20)

    response = api_client.get(f'/api/v1/courses/?name={courses[14].name}')
    courses_count = Course.objects.filter(name=courses[14].name).count()

    assert response.status_code == 200
    assert len(response.json()) == courses_count
    assert response.json()[0]['name'] == courses[14].name

@pytest.mark.django_db
def test_create_course(api_client):
    course = {'name': 'brand new course'}
    courses_count = Course.objects.count()

    response = api_client.post('/api/v1/courses/', data=course)

    assert response.status_code == 201
    assert response.json()['name'] == course['name']
    assert Course.objects.count() == courses_count + 1

@pytest.mark.django_db
def test_change_course(api_client, course_factory):
    courses = course_factory(_quantity=1)
    update = {'name': 'brand new course'}

    response = api_client.patch(
        f'/api/v1/courses/{courses[0].id}/',
        data=update,
    )

    assert response.status_code == 200
    assert response.json()['name'] != courses[0].name
    assert response.json()['name'] == update['name']

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    courses = course_factory(_quantity=1)

    response = api_client.delete(f'/api/v1/courses/{courses[0].id}/')

    assert response.status_code == 204
    assert Course.objects.filter(id=courses[0].id).count() == 0
