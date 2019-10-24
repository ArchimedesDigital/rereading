"""
Models for the Rereading app.
"""
from ast import literal_eval

from django.db import models


class Document(models.Model):
    """
    A single document (story, novel, etc.) for reading.
    This model holds the metadata for the story.
    The text itself is stored in the Segment model, which holds
    one text segment and its sequence within the document.
    """
    title = models.CharField(
        max_length=255,
    )

    author = models.CharField(
        blank=True,
        max_length=255,
    )


class Segment(models.Model):
    """
    A segment of a Document.
    """
    text = models.TextField(default='')
    sequence = models.IntegerField()  # position of this segment in the doc

    document = models.ForeignKey(
        Document,
        null=False,
        on_delete=models.CASCADE,
        related_name='segments',
    )

    class Meta:
        # see: https://docs.djangoproject.com/en/2.2/ref/models/options/#unique-together
        unique_together = [
            ['document', 'sequence'],
        ]


class Student(models.Model):
    """
    A user who reads stories and responds to questions.
    """
    name = models.TextField(default='')


class SegmentQuestion(models.Model):
    """
    A model that represents a question about a given segment
    """
    text = models.TextField()
    response_word_limit = models.IntegerField()
    segment = models.ForeignKey(
        Segment,
        on_delete=models.CASCADE,
        related_name='questions'
    )


class SegmentQuestionResponse(models.Model):
    question = models.ForeignKey(
        SegmentQuestion,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
    )
    response = models.TextField(blank=True)


class SegmentContext(models.Model):
    """
    A model representing a given context provided to a document segment
    """
    text = models.TextField()
    segment = models.ForeignKey(
        Segment,
        null=False,
        on_delete=models.CASCADE,
        related_name='contexts'
    )


class StudentReadingData(models.Model):
    """
    A model to capture the data for a single reading by a student
    """
    student = models.ForeignKey(
        Student,
        null=False,
        on_delete=models.CASCADE,
        related_name='reading_data'
    )

    document = models.ForeignKey(
        Document,
        null=False,
        on_delete=models.CASCADE,
        related_name='reading_data'
    )


class StudentSegmentData(models.Model):
    """
    A model to capture data per segment (timing, scrolls, etc.)
    """
    segment = models.ForeignKey(
        Segment,
        null=False,
        on_delete=models.CASCADE,
        related_name='segment_data'
    )

    reading_data = models.ForeignKey(
        StudentReadingData,
        null=False,
        on_delete=models.CASCADE,
        related_name='segment_data'
    )
    views = models.TextField(default='[]')
    scroll_ups = models.IntegerField(default=0)

    def get_parsed_views(self):
        """
        Views are stored as a string representing JSON data, so it needs to be converted
        into a Python object before much can be done with it.
        """

        return literal_eval(self.views)


################################################################################
# PROTOTYPING MODELS
# The models below were in use for the summer prototype and initial development
# of the rereading app.
################################################################################
class StoryPrototype(models.Model):
    """
    A single story with its text.
    """
    story_text = models.TextField()

    def __str___(self):
        return self.story_text


class ContextPrototype(models.Model):
    """
    The Context in which a story is read.
    """
    text = models.TextField()
    story = models.ForeignKey(
        StoryPrototype,
        on_delete=models.CASCADE,
        related_name='contexts',
    )

    def __str__(self):
        return self.text


class QuestionPrototype(models.Model):
    """
    A question about a Story.
    """
    text = models.TextField()
    word_limit = models.IntegerField()
    story = models.ForeignKey(
        StoryPrototype,
        on_delete=models.CASCADE,
        related_name='questions',
    )

    def __str__(self):
        return self.text


class StudentResponsePrototype(models.Model):
    """
    The response of a student to a question given a context.
    """
    question = models.ForeignKey(
        QuestionPrototype,
        null=True,
        on_delete=models.SET_NULL,
        related_name='student_responses',
    )
    context = models.ForeignKey(
        ContextPrototype,
        null=True,
        on_delete=models.SET_NULL,
        related_name='student_responses',
    )

    response = models.TextField(default='')
    views = models.TextField(default='')  # do not use me directly! see get_parsed_views()
    scroll_ups = models.IntegerField(default=0)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,  # if the Student is deleted, all her/his responses are too.
        related_name='student_responses',
    )

    def get_parsed_views(self):
        """
        Since views are stored as a TextField directly as the JSON representation
        of a list of floats, we need to convert this to a Python object in order
        to use it in our analyses.
        """

        return literal_eval(self.views)
