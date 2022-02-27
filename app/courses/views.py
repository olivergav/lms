from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateResponseMixin, View

from .forms import ModuleFormset
from .models import Course


class CreateCourse(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	model = Course
	fields = ['title', 'subject', 'slug', 'overview']
	template_name = 'courses/create_course.html'
	permission_required = 'course.add_course'
	login_url = reverse_lazy('login')
	raise_exception = True
	success_url = reverse_lazy('courses:home')

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)


class CourseModuleUpdateView(TemplateResponseMixin, View):
	template_name = 'courses/add_modules_course.html'
	course = None

	def get_formset(self, data=None):
		return ModuleFormset(instance=self.course, data=data)

	def dispatch(self, request, *args, **kwargs):
		self.course = get_object_or_404(Course, id=kwargs['pk'], owner=request.user)
		return super().dispatch(request, kwargs['pk'])

	def get(self, request, *args, **kwargs):
		formset = self.get_formset()
		return self.render_to_response({'course': self.course, 'formset': formset})

	def post(self, request, *args, **kwargs):
		formset = self.get_formset(data=request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('courses:home')
		return self.render_to_response({'course': self.course, 'formset': formset})

