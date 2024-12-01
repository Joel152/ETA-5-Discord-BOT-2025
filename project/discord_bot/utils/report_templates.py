"""
Pre-made report templates for the DMT command
"""

REPORT_TEMPLATES = {
    "spam": {
        "title": "Spam Report",
        "description": "User reported for spamming in the channel.",
        "color": 0xFF0000  # Red
    },
    "harassment": {
        "title": "Harassment Report",
        "description": "User reported for harassment.",
        "color": 0xFF0000  # Red
    },
    "nsfw": {
        "title": "NSFW Content",
        "description": "User posted inappropriate content.",
        "color": 0xFF0000  # Red
    },
    "raid": {
        "title": "Raid Alert",
        "description": "Potential raid detected.",
        "color": 0xFF4500  # Orange Red
    },
    "other": {
        "title": "General Report",
        "description": "General moderation assistance needed.",
        "color": 0xFFA500  # Orange
    }
}
