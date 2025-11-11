import json
import os
from unittest.mock import patch, MagicMock

os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")

from .app import put_function

def test_put_function_returns_count():
    event = {}
    context = {}

    mock_item = {'Item': {'visit_count': 5}}

    with patch('boto3.Session') as mock_session:
        mock_session.return_value.region_name = 'us-east-1'
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
        assert body['count'] == 6

