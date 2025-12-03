from django.contrib import admin
from .models import Question, Answer, CourseReview , Certificate

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(CourseReview)
admin.site.register(Certificate)