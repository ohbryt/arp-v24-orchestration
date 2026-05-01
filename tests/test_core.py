"""
ARP v24 Orchestration - Core Tests
Basic unit tests for core modules
"""

import pytest
import sys
sys.path.insert(0, '.')

# Import from agents since core modules aren't defined yet
# These tests validate the infrastructure


class TestInfrastructure:
    """Test basic infrastructure"""

    def test_imports(self):
        """Test that required modules can be imported"""
        from agents.hypothesis_agent import HypothesisAgent, Hypothesis
        from agents.experiment_agent import ExperimentAgent, ExperimentProtocol
        assert True

    def test_hypothesis_dataclass(self):
        """Test Hypothesis dataclass"""
        from agents.hypothesis_agent import Hypothesis

        h = Hypothesis(
            id="test_1",
            target="KDM4A",
            disease="lung_cancer",
            description="Test",
            mechanism="Mechanism",
            predicted_outcome="Outcome",
            supporting_evidence=["E1"],
            testable_predictions=["P1"],
            confidence=0.8,
            priority="high"
        )

        assert h.id == "test_1"
        assert h.target == "KDM4A"
        assert h.confidence == 0.8
        assert h.priority == "high"

    def test_experiment_protocol_dataclass(self):
        """Test ExperimentProtocol dataclass"""
        from agents.experiment_agent import ExperimentProtocol

        p = ExperimentProtocol(
            id="prot_1",
            hypothesis_id="hyp_1",
            title="Test Protocol",
            objective="Objective",
            method="Method",
            readouts=["R1"],
            controls=["C1"],
            sample_size=3,
            duration_days=7,
            resources=["Res1"],
            steps=[{"step": 1, "action": "A1", "time": "T1"}],
            expected_results="Results",
            statistical_analysis="t-test"
        )

        assert p.id == "prot_1"
        assert p.sample_size == 3
        assert p.duration_days == 7


class TestHypothesisAgent:
    """Test HypothesisAgent functionality"""

    def test_agent_initialization(self):
        """Test agent can be initialized"""
        from agents.hypothesis_agent import HypothesisAgent

        agent = HypothesisAgent()
        assert agent is not None
        assert agent.hypotheses == []
        assert agent.history == []

    def test_agent_with_config(self):
        """Test agent with config"""
        from agents.hypothesis_agent import HypothesisAgent

        config = {"llm_provider": "groq", "model": "llama-3.3-70b"}
        agent = HypothesisAgent(config=config)
        assert agent.llm_provider == "groq"
        assert agent.model == "llama-3.3-70b"


class TestExperimentAgent:
    """Test ExperimentAgent functionality"""

    def test_agent_initialization(self):
        """Test agent can be initialized"""
        from agents.experiment_agent import ExperimentAgent

        agent = ExperimentAgent()
        assert agent is not None
        assert "in_vitro" in agent.templates
        assert "in_vivo" in agent.templates

    def test_templates_structure(self):
        """Test templates have expected structure"""
        from agents.experiment_agent import ExperimentAgent

        agent = ExperimentAgent()

        # in_vitro should have these assays
        in_vitro_templates = agent.templates["in_vitro"]
        assert "cell_viability" in in_vitro_templates
        assert "qpcr" in in_vitro_templates
        assert "western_blot" in in_vitro_templates
        assert "ferroptosis_assay" in in_vitro_templates

        # in_vivo should have these models
        in_vivo_templates = agent.templates["in_vivo"]
        assert "xenograft" in in_vivo_templates
        assert "fibrosis_model" in in_vivo_templates

    def test_sample_size_calculation(self):
        """Test sample size varies by model"""
        from agents.experiment_agent import ExperimentAgent

        agent = ExperimentAgent()

        assert agent._calculate_sample_size("in_vitro") == 3
        assert agent._calculate_sample_size("in_vivo") == 8

    def test_default_controls(self):
        """Test default controls"""
        from agents.experiment_agent import ExperimentAgent

        agent = ExperimentAgent()

        in_vitro_controls = agent._get_default_controls("in_vitro")
        assert "Untreated control" in in_vitro_controls
        assert "Vehicle control" in in_vitro_controls

        in_vivo_controls = agent._get_default_controls("in_vivo")
        assert "Sham control" in in_vivo_controls
        assert "Model control" in in_vivo_controls
