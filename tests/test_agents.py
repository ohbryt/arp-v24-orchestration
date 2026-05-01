"""
ARP v24 Orchestration - Agent Tests
Tests for HypothesisAgent and ExperimentAgent
"""

import pytest
import sys
sys.path.insert(0, '.')

from agents.hypothesis_agent import HypothesisAgent, Hypothesis
from agents.experiment_agent import ExperimentAgent, ExperimentProtocol


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
        h = Hypothesis(
            id="test_1",
            target="KDM4A",
            disease="lung_cancer",
            description="Test hypothesis",
            mechanism="Test mechanism",
            predicted_outcome="Test outcome",
            supporting_evidence=["Evidence 1"],
            testable_predictions=["Prediction 1"],
            confidence=0.5,
            priority="medium"
        )

        # Add mock hypothesis
        agent.hypotheses.append(h)

        # Test retrieval
        results = agent.get_hypotheses(target="KDM4A")
        assert len(results) == 1

        results = agent.get_hypotheses(target="nonexistent")
        assert len(results) == 0

    def test_rank_hypotheses(self):
        """Test hypothesis ranking"""
        agent = HypothesisAgent()

        # Add mock hypotheses with different confidence
        agent.hypotheses.append(Hypothesis(
            id="low",
            target="KDM4A",
            disease="lung_cancer",
            description="Low confidence",
            mechanism="",
            predicted_outcome="",
            supporting_evidence=[],
            testable_predictions=[],
            confidence=0.3,
            priority="low"
        ))
        agent.hypotheses.append(Hypothesis(
            id="high",
            target="KDM4A",
            disease="lung_cancer",
            description="High confidence",
            mechanism="",
            predicted_outcome="",
            supporting_evidence=[],
            testable_predictions=[],
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
        protocol = ExperimentProtocol(
            id="prot_1",
            hypothesis_id="hyp_1",
            title="Test Protocol",
            objective="Test objective",
            method="Test method",
            readouts=["Readout 1"],
            controls=["Control 1"],
            sample_size=3,
            duration_days=7,
            resources=["Resource 1"],
            steps=[{"step": 1, "action": "Do something", "time": "Day 1"}],
            expected_results="Expected",
            statistical_analysis="t-test"
        )

        agent.protocols.append(protocol)

        results = agent.get_protocols()
        assert len(results) == 1

        results = agent.get_protocols(hypothesis_id="hyp_2")
        assert len(results) == 0

    def test_templates(self):
        """Test that templates are available"""
        agent = ExperimentAgent()

        # Check in_vitro templates
        assert "cell_viability" in agent.templates["in_vitro"]
        assert "qpcr" in agent.templates["in_vitro"]
        assert "western_blot" in agent.templates["in_vitro"]
        assert "ferroptosis_assay" in agent.templates["in_vitro"]

        # Check in_vivo templates
        assert "xenograft" in agent.templates["in_vivo"]
        assert "fibrosis_model" in agent.templates["in_vivo"]
