# get_function/test_basic.py
import json
from unittest.mock import patch, MagicMock

from .app import put_function

def test_put_function_returns_count():
    event = {}
    context = {}

    mock_item = {'Item': {'visit_count': 5}}

    with patch('boto3.Session') as mock_session:
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()
        mock_table.get_item.return_value = mock_item
        mock_table.put_item.return_value = {}
        mock_table.update_item.return_value = {}
        mock_dynamodb.Table.return_value = mock_table
        mock_session.return_value.resource.return_value = mock_dynamodb

        result = put_function(event, context)

        assert result['statusCode'] == 200
        body = json.loads(result['body'])
        assert body['count'] == 6  # 5 from DB + 1

