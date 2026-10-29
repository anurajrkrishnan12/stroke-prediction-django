from django import template

register = template.Library()

@register.filter
def employment_type(work_type):
    """Convert work type code to professional display name"""
    employment_types = {
        'Private': '🏢 Private Sector',
        'Self-employed': '💼 Self-employed / Entrepreneur',
        'Govt_job': '🏛️ Public Sector / Government',
        'children': '👨‍🎓 Student',
        'Never_worked': '📋 Unemployed / Job Seeker'
    }
    return employment_types.get(work_type, work_type)
