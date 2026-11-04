"""Unit tests for job definition retrieval."""
import json

import pytest


@pytest.fixture(autouse=True)
def use_add_agent_to_path(add_agent_to_path):
    pass


def test_get_job_definitions_returns_list():
    """GET_JobDefinition mock returns a list of job definitions."""
    mock_data_path = __file__.replace("tests/test_get_job_definitions.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    definitions = mock_data["servers"]["afc-scheduling-spi"]["tools"]["GET_JobDefinition"]["mock_response"]
    assert isinstance(definitions, list)
    assert len(definitions) >= 1


def test_job_definitions_have_required_fields():
    """Each job definition has name and version."""
    mock_data_path = __file__.replace("tests/test_get_job_definitions.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    definitions = mock_data["servers"]["afc-scheduling-spi"]["tools"]["GET_JobDefinition"]["mock_response"]
    for jd in definitions:
        assert "name" in jd
        assert "version" in jd
        assert "description" in jd


def test_task_definitions_returned():
    """provider_getTaskDefinitions mock returns task definitions."""
    mock_data_path = __file__.replace("tests/test_get_job_definitions.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    result = mock_data["servers"]["afc-task-provider-v2"]["tools"]["provider_getTaskDefinitions"]["mock_response"]
    assert "value" in result
    assert len(result["value"]) >= 1
    for td in result["value"]:
        assert "urn" in td
        assert "name" in td
