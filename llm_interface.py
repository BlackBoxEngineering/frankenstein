"""
LLM Interface - Abstract interface for external LLMs
Supports OpenAI, Anthropic, and local models
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Response from LLM"""
    content: str
    model: str
    reasoning: Optional[str] = None
    confidence: float = 0.5


class LLMInterface(ABC):
    """Abstract interface for LLM providers"""
    
    @abstractmethod
    def query(self, prompt: str, context: Optional[str] = None) -> LLMResponse:
        """Send query to LLM with optional context"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if LLM is available"""
        pass


class OpenAIInterface(LLMInterface):
    """OpenAI GPT interface"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self._client = None
        
        if api_key:
            try:
                import openai
                self._client = openai.OpenAI(api_key=api_key)
            except ImportError:
                pass
    
    def query(self, prompt: str, context: Optional[str] = None) -> LLMResponse:
        """Query OpenAI API"""
        if not self._client:
            raise RuntimeError("OpenAI client not initialized")
        
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})
        
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1  # Low temperature for logical reasoning
        )
        
        return LLMResponse(
            content=response.choices[0].message.content,
            model=self.model,
            confidence=0.8
        )
    
    def is_available(self) -> bool:
        """Check if OpenAI is available"""
        return self._client is not None


class AnthropicInterface(LLMInterface):
    """Anthropic Claude interface"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key
        self.model = model
        self._client = None
        
        if api_key:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=api_key)
            except ImportError:
                pass
    
    def query(self, prompt: str, context: Optional[str] = None) -> LLMResponse:
        """Query Anthropic API"""
        if not self._client:
            raise RuntimeError("Anthropic client not initialized")
        
        system_prompt = context if context else ""
        
        response = self._client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        return LLMResponse(
            content=response.content[0].text,
            model=self.model,
            confidence=0.8
        )
    
    def is_available(self) -> bool:
        """Check if Anthropic is available"""
        return self._client is not None


class LLMManager:
    """Manages multiple LLM providers with fallback"""
    
    def __init__(self):
        self.providers = []
    
    def add_provider(self, provider: LLMInterface):
        """Add an LLM provider"""
        if provider.is_available():
            self.providers.append(provider)
    
    def query(self, prompt: str, context: Optional[str] = None) -> Optional[LLMResponse]:
        """Query first available LLM"""
        for provider in self.providers:
            try:
                return provider.query(prompt, context)
            except Exception as e:
                continue
        return None
    
    def has_llm(self) -> bool:
        """Check if any LLM is available"""
        return len(self.providers) > 0
