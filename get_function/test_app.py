import json
from unittest.mock import patch, MagicMock

from get_function.app import get_function

def test_get_function_returns_count():
    event = {}
    context = {}

    mock_item = {'Item': {'visit_count': 5}}

    with patch('boto3.Session') as mock_session:
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()
        mock_table.get_item.return_value = mock_item
        mock_dynamodb.Table.return_value = mock_table
        mock_session.return_value.resource.return_value = mock_dynamodb

        result = get_function(event, context)

        assert result['statusCode'] == 200
        body = json.loads(result['body'])
        assert body['count'] == 5
