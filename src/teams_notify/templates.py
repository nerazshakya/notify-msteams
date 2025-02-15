from typing import Dict, Any

class CardTemplate:
    def get_template(self, template_type: str, **kwargs) -> Dict[str, Any]:
        """Get card template by type"""
        templates = {
            "basic": self._basic_template,
            "detailed": self._detailed_template,
            "error": self._error_template
        }
        
        template_func = templates.get(template_type, self._basic_template)
        return template_func(**kwargs)
    
    def _basic_template(self, title: str, message: str, **_) -> Dict[str, Any]:
        return {
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "size": "Medium",
                    "weight": "Bolder",
                    "text": title
                },
                {
                    "type": "TextBlock",
                    "text": message,
                    "wrap": True
                }
            ],
            "version": "1.0"
        }
    
    def _detailed_template(self, title: str, message: str, **kwargs) -> Dict[str, Any]:
        return {
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "size": "Medium",
                    "weight": "Bolder",
                    "text": title
                },
                {
                    "type": "TextBlock",
                    "text": message,
                    "wrap": True
                },
                {
                    "type": "FactSet",
                    "facts": [
                        {
                            "title": "Status",
                            "value": kwargs.get("status", "N/A")
                        },
                        {
                            "title": "Environment",
                            "value": kwargs.get("environment", "N/A")
                        },
                        {
                            "title": "Timestamp",
                            "value": kwargs.get("timestamp", "N/A")
                        }
                    ]
                }
            ],
            "version": "1.0"
        }
    
    def _error_template(self, title: str, message: str, **_) -> Dict[str, Any]:
        return {
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "size": "Medium",
                    "weight": "Bolder",
                    "text": "❌ " + title,
                    "color": "Attention"
                },
                {
                    "type": "TextBlock",
                    "text": message,
                    "wrap": True,
                    "color": "Attention"
                }
            ],
            "version": "1.0"
        }
