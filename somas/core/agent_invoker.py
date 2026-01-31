"""
Direct LLM API integration for autonomous agent execution.

This module provides direct API integration with OpenAI and Anthropic LLMs,
enabling autonomous agent execution without relying on GitHub Copilot
comment-driven orchestration.

Security Considerations:
- API keys must be stored in GitHub Secrets
- Input validation on all project IDs and file paths
- Path traversal prevention for artifact access
"""

import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

# Optional imports - gracefully handle if not installed
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


logger = logging.getLogger(__name__)


class AgentInvoker:
    """
    Invokes SOMAS agents using direct LLM API calls.
    
    Supports both OpenAI (GPT-4o) and Anthropic (Claude) models.
    """
    
    # Valid project ID pattern (prevents path traversal)
    PROJECT_ID_PATTERN = re.compile(r'^project-\d+$')
    
    def __init__(self, config_path: str = ".somas/config.yml"):
        """
        Initialize the agent invoker.
        
        Args:
            config_path: Path to SOMAS configuration file
        """
        self.config_path = Path(config_path)
        self.agents_dir = Path(".github/agents")
        self.config = self._load_config()
        
        # Initialize API clients if keys are available
        self.openai_client = None
        self.anthropic_client = None
        
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.openai_client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            logger.info("OpenAI client initialized")
        
        if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
            self.anthropic_client = Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            logger.info("Anthropic client initialized")
    
    def _validate_project_id(self, project_id: str) -> bool:
        """
        Validate project ID format to prevent path traversal attacks.
        
        Args:
            project_id: Project identifier to validate
            
        Returns:
            True if valid, False otherwise
        """
        return bool(self.PROJECT_ID_PATTERN.match(project_id))
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load agent configuration from .somas/config.yml
        
        Returns:
            Configuration dictionary
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path) as f:
            return yaml.safe_load(f)
    
    def _load_agent_prompt(self, agent_name: str) -> str:
        """
        Load agent prompt from .github/agents/somas-{agent_name}.md
        
        Args:
            agent_name: Name of the agent (e.g., 'planner', 'specifier')
            
        Returns:
            Agent prompt/instructions as string
        """
        agent_file = self.agents_dir / f"somas-{agent_name}.md"
        
        if not agent_file.exists():
            raise FileNotFoundError(f"Agent file not found: {agent_file}")
        
        content = agent_file.read_text()
        
        # Extract main content (skip YAML frontmatter if present)
        if content.startswith("---"):
            parts = content.split("---", 2)
            return parts[2].strip() if len(parts) > 2 else content
        
        return content
    
    def _get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Agent configuration dictionary
        """
        agent_configs = self.config.get('agents', {}).get('agent_configs', {})
        return agent_configs.get(agent_name, {})
    
    def _build_context_message(
        self, 
        context: Dict[str, Any], 
        project_id: str
    ) -> str:
        """
        Build context message from artifacts and requirements.
        
        Args:
            context: Dictionary with input artifacts and requirements
            project_id: Project identifier
            
        Returns:
            Formatted context message
        """
        message_parts = [
            f"**Project ID:** {project_id}",
            "",
            "**Context:**",
            ""
        ]
        
        for key, value in context.items():
            if isinstance(value, (Path, str)):
                # Check if it's a file path
                path = Path(value) if isinstance(value, str) else value
                
                if path.exists() and path.is_file():
                    # Include file content
                    message_parts.append(f"### {key} (from {path})")
                    message_parts.append(f"```")
                    message_parts.append(path.read_text())
                    message_parts.append("```")
                    message_parts.append("")
                else:
                    message_parts.append(f"- **{key}:** {value}")
            else:
                # Include value directly
                message_parts.append(f"- **{key}:** {value}")
        
        return "\n".join(message_parts)
    
    def _invoke_openai(
        self, 
        model: str, 
        system_prompt: str, 
        user_message: str,
        temperature: float = 0.3
    ) -> str:
        """
        Invoke OpenAI API.
        
        Args:
            model: Model name (e.g., 'gpt-4o')
            system_prompt: System prompt/instructions
            user_message: User message with context
            temperature: Sampling temperature (0.0-1.0)
            
        Returns:
            Model response as string
        """
        if not self.openai_client:
            raise RuntimeError(
                "OpenAI client not initialized. "
                "Ensure OPENAI_API_KEY is set and openai package is installed."
            )
        
        logger.info(f"Invoking OpenAI model: {model}")
        
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature
        )
        
        return response.choices[0].message.content
    
    def _invoke_anthropic(
        self, 
        model: str, 
        system_prompt: str, 
        user_message: str,
        temperature: float = 0.3
    ) -> str:
        """
        Invoke Anthropic API.
        
        Args:
            model: Model name (e.g., 'claude-3-5-sonnet-20241022')
            system_prompt: System prompt/instructions
            user_message: User message with context
            temperature: Sampling temperature (0.0-1.0)
            
        Returns:
            Model response as string
        """
        if not self.anthropic_client:
            raise RuntimeError(
                "Anthropic client not initialized. "
                "Ensure ANTHROPIC_API_KEY is set and anthropic package is installed."
            )
        
        logger.info(f"Invoking Anthropic model: {model}")
        
        response = self.anthropic_client.messages.create(
            model=model,
            max_tokens=4096,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        return response.content[0].text
    
    def invoke_agent(
        self, 
        agent_name: str, 
        context: Dict[str, Any],
        project_id: str,
        temperature: Optional[float] = None
    ) -> str:
        """
        Invoke an agent with given context using direct LLM API.
        
        Args:
            agent_name: Agent to invoke (e.g., 'planner', 'specifier')
            context: Dictionary with input artifacts and requirements
            project_id: Project identifier (e.g., 'project-123')
            temperature: Optional temperature override
            
        Returns:
            Agent response as string
            
        Raises:
            ValueError: If project_id is invalid or agent not configured
            FileNotFoundError: If agent prompt file not found
            RuntimeError: If required LLM client not available
        """
        # Validate project ID
        if not self._validate_project_id(project_id):
            raise ValueError(
                f"Invalid project ID format: {project_id}. "
                "Must match pattern: project-\\d+"
            )
        
        logger.info(f"Invoking agent: {agent_name} for project: {project_id}")
        
        # Load agent configuration
        agent_config = self._get_agent_config(agent_name)
        if not agent_config:
            raise ValueError(f"No configuration found for agent: {agent_name}")
        
        # Determine provider and model
        provider = agent_config.get('provider', 'copilot')
        providers_config = self.config.get('agents', {}).get('providers', {})
        provider_config = providers_config.get(provider, {})
        model = provider_config.get('model', 'gpt-4o')
        
        # Get temperature (use provided, or from config, or default)
        if temperature is None:
            temperature = provider_config.get('temperature', 0.3)
        
        # Load agent prompt
        system_prompt = self._load_agent_prompt(agent_name)
        
        # Build user message with context
        user_message = self._build_context_message(context, project_id)
        
        # Make API call based on provider
        if provider in ['openai', 'copilot']:
            response = self._invoke_openai(
                model, system_prompt, user_message, temperature
            )
        elif provider == 'anthropic':
            response = self._invoke_anthropic(
                model, system_prompt, user_message, temperature
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        logger.info(f"Agent {agent_name} completed successfully")
        return response
    
    def parse_artifacts(
        self, 
        response: str, 
        expected_outputs: List[str]
    ) -> Dict[str, str]:
        """
        Parse artifacts from agent response.
        
        Extracts YAML and Markdown code blocks from the response.
        
        Args:
            response: Agent response text
            expected_outputs: List of expected output file names
            
        Returns:
            Dictionary mapping output names to content
        """
        artifacts = {}
        
        # Extract YAML code blocks
        yaml_pattern = r'```yaml\n([\s\S]*?)\n```'
        yaml_matches = re.findall(yaml_pattern, response)
        
        # Extract Markdown code blocks
        md_pattern = r'```markdown\n([\s\S]*?)\n```'
        md_matches = re.findall(md_pattern, response)
        
        # Match artifacts to expected outputs
        for output in expected_outputs:
            if output.endswith('.yml') and yaml_matches:
                artifacts[output] = yaml_matches.pop(0)
            elif output.endswith('.md') and md_matches:
                artifacts[output] = md_matches.pop(0)
        
        return artifacts
    
    def save_artifacts(
        self, 
        artifacts: Dict[str, str], 
        project_id: str
    ) -> List[Path]:
        """
        Save artifacts to project directory.
        
        Args:
            artifacts: Dictionary mapping file names to content
            project_id: Project identifier
            
        Returns:
            List of saved file paths
            
        Raises:
            ValueError: If project_id is invalid
        """
        # Validate project ID
        if not self._validate_project_id(project_id):
            raise ValueError(f"Invalid project ID format: {project_id}")
        
        # Base directory for project artifacts
        base_dir = Path(".somas/projects") / project_id / "artifacts"
        base_dir.mkdir(parents=True, exist_ok=True)
        
        saved_paths = []
        
        for filename, content in artifacts.items():
            # Validate filename (no path traversal)
            if '..' in filename or '/' in filename:
                logger.warning(f"Skipping invalid filename: {filename}")
                continue
            
            file_path = base_dir / filename
            
            # Ensure path is within base directory
            if not file_path.resolve().is_relative_to(base_dir.resolve()):
                logger.warning(f"Path traversal attempt detected: {file_path}")
                continue
            
            # Write file
            file_path.write_text(content)
            saved_paths.append(file_path)
            logger.info(f"Saved artifact: {file_path}")
        
        return saved_paths
    
    def is_available(self) -> bool:
        """
        Check if agent invoker has at least one LLM client available.
        
        Returns:
            True if at least one client is initialized
        """
        return self.openai_client is not None or self.anthropic_client is not None
    
    def get_available_providers(self) -> List[str]:
        """
        Get list of available providers.
        
        Returns:
            List of provider names that are available
        """
        providers = []
        if self.openai_client:
            providers.append('openai')
        if self.anthropic_client:
            providers.append('anthropic')
        return providers
