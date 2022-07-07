import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Student, Course


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def student_factory():
    def _factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return _factory

@pytest.fixture
def course_factory():
    def _factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return _factory