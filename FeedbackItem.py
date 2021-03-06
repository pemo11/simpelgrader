# =============================================================================
# file: FeedbackItem.py
# =============================================================================

'''
Represents a feedback item for a single submission
'''
class FeedbackItem:

    def __init__(self, id, submission):
        self.id = id
        self.submission = submission
        self.message = ""
        self.severity = "normal"
        self.totalPoints = 0
        self.checkstyleReportpath = ""
        self.jUnitReportpath = ""
        self.textCompareReportpath = ""

    def __repr__(self):
        return f"Id: {self.id} for Submission {self.submission.id}: {self.totalPoints}/{self.severity}"
