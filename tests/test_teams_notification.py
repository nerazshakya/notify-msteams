import pytest
from unittest.mock import Mock, patch
from src.teams_notification import TeamsNotifier, CardTemplate

def test_basic_template():
    template = CardTemplate()
    card = template.get_template(
        "basic",
        title="Test Title",
        message="Test Message"
    )
    assert card["type"] == "AdaptiveCard"
    assert len(card["body"]) == 2
    assert card["body"][0]["text"] == "Test Title"
    assert card["body"][1]["text"] == "Test Message"

@patch('requests.post')
def test_send_notification(mock_post):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response
    
    notifier = TeamsNotifier("https://fake-webhook.url")
    response = notifier.send_notification(
        message="Test Message",
        title="Test Title"
    )
    
    assert mock_post.called
    assert response == mock_response