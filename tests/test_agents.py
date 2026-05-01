"""
ARP v25 - Agent Tests
Tests for HypothesisAgent and ExperimentAgent
"""

import pytest
from arp_v25.agents.hypothesis_agent import HypothesisAgent, Hypothesis
from arp_v25.agents.experiment_agent import ExperimentAgent, ExperimentProtocol


class TestHypothesisAgent:
    """Test HypothesisAgent module"""
    
    def test_init(self):
        """Test agent initialization"""
        agent = HypothesisAgent()
        assert agent is not None
        assert agent.hypotheses == []
    
    def test_get_hypotheses(self):
        """Test getting stored hypotheses"""
        agent = HypothesisAgent()
        
        # Create a mock hypothesis
        from dataclasses import dataclass
        @dataclass
        class MockHypothesis:
            id: str
            target: str
            disease: str
            description: str
            mechanism: str = ""
            predicted_outcome: str = ""
            supporting_evidence: list = None
            testable_predictions: list = None
            confidence: float = 0.5
            priority: str = "medium"
            
            def __post_init__(self):
                if self.supporting_evidence is None:
                    self.supporting_evidence = []
                if self.testable_predictions is None:
                    self.testable_predictions = []
        
        # Add mock hypothesis
        agent.hypotheses.append(MockHypothesis(
            id="test_1",
            target="KDM4A",
            disease="lung_cancer",
            description="Test hypothesis"
        ))
        
        # Test retrieval
        results = agent.get_hypotheses(target="KDM4A")
        assert len(results) == 1
        
        results = agent.get_hypotheses(target="nonexistent")
        assert len(results) == 0
    
    def test_rank_hypotheses(self):
        """Test hypothesis ranking"""
        agent = HypothesisAgent()
        
        from dataclasses import dataclass
        @dataclass
        class MockHypothesis:
            id: str
            target: str
            disease: str
            description: str
            mechanism: str = ""
            predicted_outcome: str = ""
            supporting_evidence: list = None
            testable_predictions: list = None
            confidence: float = 0.5
            priority: str = "medium"
            
            def __post_init__(self):
                if self.supporting_evidence is None:
                    self.supporting_evidence = []
                if self.testable_predictions is None:
                    self.testable_predictions = []
        
        # Add mock hypotheses with different confidence
        agent.hypotheses.append(MockHypothesis(
            id="low",
            target="KDM4A",
            disease="lung_cancer",
            description="Low confidence",
            confidence=0.3,
            priority="low"
        ))
        agent.hypotheses.append(MockHypothesis(
            id="high",
            target="KDM4A",
            disease="lung_cancer",
            description="High confidence",
            confidence=0.9,
            priority="high"
        ))
        
        ranked = agent.rank_hypotheses()
        assert ranked[0].id == "high"
        assert ranked[1].id == "low"


class TestExperimentAgent:
    """Test ExperimentAgent module"""
    
    def test_init(self):
        """Test agent initialization"""
        agent = ExperimentAgent()
        assert agent is not None
        assert agent.templates is not None
        assert "in_vitro" in agent.templates
    
    def test_get_default_controls(self):
        """Test default controls"""
        agent = ExperimentAgent()
        
        controls = agent._get_default_controls("in_vitro")
        assert "Untreated control" in controls
        
        controls = agent._get_default_controls("in_vivo")
        assert "Sham control" in controls
    
    def test_calculate_sample_size(self):
        """Test sample size calculation"""
        agent = ExperimentAgent()
        
        size = agent._calculate_sample_size("in_vitro")
        assert size == 3
        
        size = agent._calculate_sample_size("in_vivo")
        assert size == 8
    
    def test_get_protocols(self):
        """Test getting stored protocols"""
        agent = ExperimentAgent()
        
        # Create mock protocol
        from dataclasses import dataclass
        @dataclass
        class MockProtocol:
            id: str
            hypothesis_id: str
            title: str
            objective: str = ""
            method: str = ""
            readouts: list = None
            controls: list = None
            sample_size: int = 3
            duration_days: int = 7
            resources: list = None
            steps: list = None
            expected_results: str = ""
            statistical_analysis: str = ""
            
            def __post_init__(self):
                if self.readouts is None:
                    self.readouts = []
                if self.controls is None:
                    self.controls = []
                if self.resources is None:
                    self.resources = []
                if self.steps is None:
                    self.steps = []
        
        agent.protocols.append(MockProtocol(
            id="prot_1",
            hypothesis_id="hyp_1",
            title="Test Protocol"
        ))
        
        results = agent.get_protocols()
        assert len(results) == 1
        
        results = agent.get_protocols(hypothesis_id="hyp_2")
        assert len(results) == 0
