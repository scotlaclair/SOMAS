"""
Tests for the AgentInvoker class.

Tests cover:
- Configuration loading
- Project ID validation
- Agent prompt loading
- API client initialization
- Context message building
- Artifact parsing and saving
"""

import os
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from somas.core.agent_invoker import AgentInvoker


@pytest.fixture
def temp_somas_dir():
    """Create temporary SOMAS directory structure"""
    temp_dir = tempfile.mkdtemp()
    
    # Create directory structure
    config_dir = Path(temp_dir) / ".somas"
    config_dir.mkdir()
    
    agents_dir = Path(temp_dir) / ".github" / "agents"
    agents_dir.mkdir(parents=True)
    
    projects_dir = config_dir / "projects"
    projects_dir.mkdir()
    
    # Create minimal config file
    config_content = """
agents:
  providers:
    openai:
      model: "gpt-4o"
      temperature: 0.3
    anthropic:
      model: "claude-3-5-sonnet-20241022"
      temperature: 0.3
  agent_configs:
    planner:
      provider: "openai"
    specifier:
      provider: "anthropic"
"""
    (config_dir / "config.yml").write_text(config_content)
    
    # Create sample agent file
    agent_content = """---
name: somas-planner
description: Test planner agent
---

# Test Planner Agent

You are a test planner agent for testing purposes.

## Instructions

Create a plan based on the provided context.
"""
    (agents_dir / "somas-planner.md").write_text(agent_content)
    
    # Change to temp directory
    original_dir = os.getcwd()
    os.chdir(temp_dir)
    
    yield temp_dir
    
    # Cleanup
    os.chdir(original_dir)
    shutil.rmtree(temp_dir)


class TestAgentInvoker:
    """Test suite for AgentInvoker"""
    
    def test_initialization(self, temp_somas_dir):
        """Test AgentInvoker initialization"""
        invoker = AgentInvoker()
        
        assert invoker.config is not None
        assert 'agents' in invoker.config
        assert invoker.agents_dir.exists()
    
    def test_validate_project_id(self, temp_somas_dir):
        """Test project ID validation"""
        invoker = AgentInvoker()
        
        # Valid project IDs
        assert invoker._validate_project_id("project-123")
        assert invoker._validate_project_id("project-1")
        assert invoker._validate_project_id("project-999999")
        
        # Invalid project IDs (path traversal attempts)
        assert not invoker._validate_project_id("../etc/passwd")
        assert not invoker._validate_project_id("project-123/../secret")
        assert not invoker._validate_project_id("project-abc")
        assert not invoker._validate_project_id("not-a-project-id")
        assert not invoker._validate_project_id("")
        assert not invoker._validate_project_id("project-")
    
    def test_load_config(self, temp_somas_dir):
        """Test configuration loading"""
        invoker = AgentInvoker()
        config = invoker._load_config()
        
        assert 'agents' in config
        assert 'providers' in config['agents']
        assert 'agent_configs' in config['agents']
        assert 'openai' in config['agents']['providers']
    
    def test_load_agent_prompt(self, temp_somas_dir):
        """Test agent prompt loading"""
        invoker = AgentInvoker()
        prompt = invoker._load_agent_prompt("planner")
        
        assert "Test Planner Agent" in prompt
        assert "Instructions" in prompt
        # Frontmatter should be stripped
        assert "---" not in prompt or prompt.count("---") < 2
    
    def test_load_agent_prompt_not_found(self, temp_somas_dir):
        """Test agent prompt loading with non-existent agent"""
        invoker = AgentInvoker()
        
        with pytest.raises(FileNotFoundError):
            invoker._load_agent_prompt("nonexistent-agent")
    
    def test_get_agent_config(self, temp_somas_dir):
        """Test getting agent configuration"""
        invoker = AgentInvoker()
        
        planner_config = invoker._get_agent_config("planner")
        assert planner_config['provider'] == 'openai'
        
        specifier_config = invoker._get_agent_config("specifier")
        assert specifier_config['provider'] == 'anthropic'
        
        # Non-existent agent returns empty dict
        unknown_config = invoker._get_agent_config("unknown")
        assert unknown_config == {}
    
    def test_build_context_message(self, temp_somas_dir):
        """Test context message building"""
        invoker = AgentInvoker()
        
        # Create test file
        test_file = Path(".somas/projects/test.txt")
        test_file.write_text("Test content")
        
        context = {
            "project_name": "Test Project",
            "priority": "high",
            "spec_file": test_file
        }
        
        message = invoker._build_context_message(context, "project-123")
        
        assert "Project ID:** project-123" in message
        assert "project_name:** Test Project" in message
        assert "priority:** high" in message
        assert "spec_file" in message
        assert "Test content" in message
    
    def test_parse_artifacts_yaml(self, temp_somas_dir):
        """Test artifact parsing from YAML code blocks"""
        invoker = AgentInvoker()
        
        response = """
Here is the plan:

```yaml
project_id: project-123
title: Test Project
features:
  - feature1
  - feature2
```

This is the complete plan.
"""
        
        artifacts = invoker.parse_artifacts(response, ["initial_plan.yml"])
        
        assert "initial_plan.yml" in artifacts
        assert "project_id: project-123" in artifacts["initial_plan.yml"]
        assert "features:" in artifacts["initial_plan.yml"]
    
    def test_parse_artifacts_markdown(self, temp_somas_dir):
        """Test artifact parsing from Markdown code blocks"""
        invoker = AgentInvoker()
        
        response = """
Here is the specification:

```markdown
# Project Specification

## Requirements

- REQ-F-001: User authentication
- REQ-F-002: Data storage
```

End of specification.
"""
        
        artifacts = invoker.parse_artifacts(response, ["SPEC.md"])
        
        assert "SPEC.md" in artifacts
        assert "# Project Specification" in artifacts["SPEC.md"]
        assert "REQ-F-001" in artifacts["SPEC.md"]
    
    def test_save_artifacts(self, temp_somas_dir):
        """Test artifact saving"""
        invoker = AgentInvoker()
        
        artifacts = {
            "test_plan.yml": "project_id: project-123\ntitle: Test",
            "README.md": "# Test README"
        }
        
        saved_paths = invoker.save_artifacts(artifacts, "project-123")
        
        assert len(saved_paths) == 2
        
        # Verify files exist and have correct content
        for path in saved_paths:
            assert path.exists()
            content = path.read_text()
            assert len(content) > 0
    
    def test_save_artifacts_invalid_project_id(self, temp_somas_dir):
        """Test artifact saving with invalid project ID"""
        invoker = AgentInvoker()
        
        artifacts = {"test.yml": "content"}
        
        with pytest.raises(ValueError):
            invoker.save_artifacts(artifacts, "../etc/passwd")
    
    def test_save_artifacts_path_traversal_prevention(self, temp_somas_dir):
        """Test that path traversal in filenames is prevented"""
        invoker = AgentInvoker()
        
        # Attempt path traversal in filename
        artifacts = {
            "../../../etc/passwd": "malicious",
            "../../secret.txt": "data"
        }
        
        saved_paths = invoker.save_artifacts(artifacts, "project-123")
        
        # No files should be saved due to validation
        assert len(saved_paths) == 0
    
    def test_is_available_no_clients(self, temp_somas_dir):
        """Test availability check when no clients initialized"""
        invoker = AgentInvoker()
        invoker.openai_client = None
        invoker.anthropic_client = None
        
        assert not invoker.is_available()
    
    def test_get_available_providers(self, temp_somas_dir):
        """Test getting available providers"""
        invoker = AgentInvoker()
        
        # Mock clients
        invoker.openai_client = Mock()
        invoker.anthropic_client = None
        
        providers = invoker.get_available_providers()
        assert 'openai' in providers
        assert 'anthropic' not in providers
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_invoke_openai(self, temp_somas_dir):
        """Test OpenAI API invocation"""
        invoker = AgentInvoker()
        
        # Mock OpenAI client
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        
        invoker.openai_client = Mock()
        invoker.openai_client.chat.completions.create.return_value = mock_response
        
        result = invoker._invoke_openai(
            "gpt-4o",
            "System prompt",
            "User message",
            0.3
        )
        
        assert result == "Test response"
        invoker.openai_client.chat.completions.create.assert_called_once()
    
    def test_invoke_openai_not_available(self, temp_somas_dir):
        """Test OpenAI invocation when client not available"""
        invoker = AgentInvoker()
        invoker.openai_client = None
        
        with pytest.raises(RuntimeError, match="OpenAI client not initialized"):
            invoker._invoke_openai("gpt-4o", "system", "user", 0.3)
    
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'})
    def test_invoke_anthropic(self, temp_somas_dir):
        """Test Anthropic API invocation"""
        invoker = AgentInvoker()
        
        # Mock Anthropic client
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Test response"
        
        invoker.anthropic_client = Mock()
        invoker.anthropic_client.messages.create.return_value = mock_response
        
        result = invoker._invoke_anthropic(
            "claude-3-5-sonnet-20241022",
            "System prompt",
            "User message",
            0.3,
            4096
        )
        
        assert result == "Test response"
        invoker.anthropic_client.messages.create.assert_called_once()
    
    def test_invoke_anthropic_not_available(self, temp_somas_dir):
        """Test Anthropic invocation when client not available"""
        invoker = AgentInvoker()
        invoker.anthropic_client = None
        
        with pytest.raises(RuntimeError, match="Anthropic client not initialized"):
            invoker._invoke_anthropic("claude", "system", "user", 0.3, 4096)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_invoke_agent_full_flow(self, temp_somas_dir):
        """Test full agent invocation flow"""
        invoker = AgentInvoker()
        
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Agent response"
        
        invoker.openai_client = Mock()
        invoker.openai_client.chat.completions.create.return_value = mock_response
        
        context = {"requirement": "Build a chat app"}
        
        result = invoker.invoke_agent("planner", context, "project-123")
        
        assert result == "Agent response"
        invoker.openai_client.chat.completions.create.assert_called_once()
    
    def test_invoke_agent_invalid_project_id(self, temp_somas_dir):
        """Test agent invocation with invalid project ID"""
        invoker = AgentInvoker()
        
        with pytest.raises(ValueError, match="Invalid project ID"):
            invoker.invoke_agent("planner", {}, "../etc/passwd")
    
    def test_invoke_agent_unknown_agent(self, temp_somas_dir):
        """Test agent invocation with unknown agent"""
        invoker = AgentInvoker()
        
        with pytest.raises(ValueError, match="No configuration found"):
            invoker.invoke_agent("unknown-agent", {}, "project-123")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
