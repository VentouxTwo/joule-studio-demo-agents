"""Tests for the mcp_tools indirection layer and skill loading."""
import pytest
from pathlib import Path


def test_mcp_tools_module_importable():
    """mcp_tools module must be importable from app/."""
    import mcp_tools
    assert hasattr(mcp_tools, "get_mcp_tools")


def test_get_mcp_tools_is_callable():
    import mcp_tools
    import inspect
    assert callable(mcp_tools.get_mcp_tools)


@pytest.mark.asyncio
async def test_get_mcp_tools_returns_list(patch_mcp_tools):
    """In test mode, get_mcp_tools() must return a list of tools."""
    import mcp_tools
    tools = await mcp_tools.get_mcp_tools()
    assert isinstance(tools, list)
    assert len(tools) > 0


def test_goal_setting_skill_exists():
    """The goal-setting-workflow SKILL.md must exist."""
    skill_path = Path(__file__).parent.parent / "app" / "skills" / "goal-setting-workflow" / "SKILL.md"
    assert skill_path.exists(), f"SKILL.md not found at {skill_path}"


def test_goal_setting_skill_has_frontmatter():
    """SKILL.md must have YAML frontmatter with name and description."""
    skill_path = Path(__file__).parent.parent / "app" / "skills" / "goal-setting-workflow" / "SKILL.md"
    content = skill_path.read_text()
    assert "name: goal-setting-workflow" in content
    assert "description:" in content


def test_goal_setting_skill_covers_five_steps():
    """SKILL.md must cover all 5 workflow steps."""
    skill_path = Path(__file__).parent.parent / "app" / "skills" / "goal-setting-workflow" / "SKILL.md"
    content = skill_path.read_text()
    assert "Step 1" in content
    assert "Step 2" in content
    assert "Step 3" in content
    assert "Step 4" in content
    assert "Step 5" in content


def test_goal_setting_skill_has_confirmation_gate():
    """SKILL.md must have an explicit confirmation gate before writing goals."""
    skill_path = Path(__file__).parent.parent / "app" / "skills" / "goal-setting-workflow" / "SKILL.md"
    content = skill_path.read_text()
    assert "explicit" in content.lower()
    assert "confirm" in content.lower()
