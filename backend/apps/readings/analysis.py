"""

Analysis.py - analyses for dhmit/rereading wired into the webapp

"""
from .models import StudentResponse
import statistics


class RereadingAnalysis:
    """
    This class loads all student responses from the db,
    and implements analysis methods on these responses.

    We use .serializers.AnalysisSerializer to send these analysis results to the
    frontend for display.
    """

    def __init__(self):
        """ On initialization, we load all of the StudentResponses from the db """
        self.responses = StudentResponse.objects.all()

    @property
    def total_view_time(self):
        """
        Queries the db for all StudentResponses,
        and computes total time (across all users) spent reading the text

        :return: float, the total time all users spent reading the text
        """
        total_view_time = 0
        for response in self.responses:
            for view_time in response.get_parsed_views():
                total_view_time += view_time
        return total_view_time

    @property
    def median_revisits(self):
        """
        Queries the db for all StudentResponse,
        and computes median count of revisits (across all users) spent per unique question

        :return: dict, key = question, string. value = revisits, float.
        """
        results = {}
        for response in self.responses:
            question = response.question.text
            num_views = len(response.get_parsed_views())
            result = results.get(question)
            if result:
                result.append(num_views)
            else:  # Create a key for the question
                results[question] = [num_views]

        # Compute the median
        for question in results:
            results[question] = statistics.median(results[question])

        return results


