import time

class CEOBrain:
    """The master controller that coordinates all specialist brains."""
    def __init__(self, brain):
        self.brain = brain
        self.is_thinking = False

    def solve_complex_task(self, user_request):
        """Phase 1: Intent & Planning."""
        print(f"[CEO] New High-Level Request: {user_request}")
        
        # 1. PERCEPTION: Get current context
        context = self.brain.vision_cortex.get_context_string()
        system_vitals = f"CPU: {self.brain.monitor.cpu_high}%" # simplified
        
        # 2. PLANNING: Ask LLM for a multi-step plan
        plan_prompt = f"""
        USER REQUEST: {user_request}
        CONTEXT: {context}
        SYSTEM: {system_vitals}
        
        TASK: Create a multi-step PLAN to achieve this. 
        Think step-by-step.
        """
        plan = self.brain.query_lm_studio(plan_prompt)
        print(f"[CEO] Plan Generated: {plan}")

        # 3. EXECUTION: Hand off steps to the Execution Brain
        # This uses the EXECUTE: protocol already in Brain
        result = self.brain.process_command(user_request)

        # 4. REFLECTION: Self-improvement loop
        self.reflect(user_request, plan, result)
        
        return result

    def reflect(self, request, plan, result):
        """Phase 4: Reflection & Learning."""
        print("[CEO] Reflecting on performance...")
        
        # Did it work?
        if "Success" in str(result) or "Complete" in str(result):
            # Save success pattern to Skill Graph
            self.brain.episodic.record_episode(request, plan, "Success", 5)
        else:
            # Analyze failure
            print(f"[CEO] Task failed or was imperfect. Logging for correction.")
            self.brain.correction.learn_from_correction(request, "optimization_needed")
