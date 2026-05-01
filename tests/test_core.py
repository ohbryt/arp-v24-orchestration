"""
ARP v25 - Core Tests
Basic unit tests for core modules
"""

import pytest
from arp_v25.core.director import Director, ResearchGoal, TaskPriority
from arp_v25.core.registry import TargetRegistry
from arp_v25.core.router import Router


class TestDirector:
    """Test Director module"""
    
    def test_create_goal(self):
        """Test goal creation"""
        director = Director()
        goal_id = director.create_goal(
            target="KDM4A",
            disease="lung_cancer",
            priority=TaskPriority.HIGH,
            description="Test hypothesis"
        )
        assert goal_id is not None
        assert director.get_status()["total_goals"] == 1
    
    def test_complete_task(self):
        """Test task completion"""
        director = Director()
        goal_id = director.create_goal(
            target="DGAT1",
            disease="nsclc"
        )
        director.complete_task(goal_id, {"result": "success"})
        assert director.get_status()["completed_tasks"] == 1


class TestTargetRegistry:
    """Test TargetRegistry module"""
    
    def test_get_target(self):
        """Test getting a target"""
        registry = TargetRegistry()
        target = registry.get("DGAT1")
        assert target is not None
        assert target.id == "DGAT1"
    
    def test_search_targets(self):
        """Test target search"""
        registry = TargetRegistry()
        results = registry.search("ferroptosis")
        assert len(results) > 0
    
    def test_filter_by_disease(self):
        """Test disease filtering"""
        registry = TargetRegistry()
        targets = registry.filter_by_disease("lung cancer")
        assert len(targets) > 0
    
    def test_list_all(self):
        """Test listing all targets"""
        registry = TargetRegistry()
        all_targets = registry.list_all()
        assert len(all_targets) >= 12  # At least 12 targets registered


class TestRouter:
    """Test Router module"""
    
    def test_route_by_target(self):
        """Test routing by target"""
        router = Router()
        agent = router.route("KDM4A", "lung_cancer")
        assert agent == "epigenetic_researcher"
    
    def test_route_by_disease(self):
        """Test routing by disease"""
        router = Router()
        agent = router.route("SLC7A11", "nsclc")
        assert agent == "ferroptosis_researcher"
    
    def test_default_route(self):
        """Test default routing"""
        router = Router()
        agent = router.route("UNKNOWN", "unknown_disease")
        assert agent == "general_researcher"
    
    def test_available_routes(self):
        """Test getting available routes"""
        router = Router()
        routes = router.get_available_routes()
        assert "by_target" in routes
        assert "by_disease" in routes


class TestOrchestrator:
    """Test Orchestrator module"""
    
    def test_register_handler(self):
        """Test handler registration"""
        from arp_v25.core.orchestrator import Orchestrator
        
        orchestrator = Orchestrator()
        
        def dummy_handler(payload):
            return {"result": "ok"}
        
        orchestrator.register_handler("test_task", dummy_handler)
        assert "test_task" in orchestrator.handlers
    
    def test_create_task(self):
        """Test task creation"""
        from arp_v25.core.orchestrator import Orchestrator
        
        orchestrator = Orchestrator()
        task_id = orchestrator.create_task("test", {"data": "test"})
        assert task_id is not None
    
    def test_queue_status(self):
        """Test queue status"""
        from arp_v25.core.orchestrator import Orchestrator
        
        orchestrator = Orchestrator()
        orchestrator.create_task("test", {})
        status = orchestrator.get_queue_status()
        assert status["total"] == 1
        assert status["pending"] == 1
