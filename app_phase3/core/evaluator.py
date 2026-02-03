from app.core.models import ProfessionalProfile, JobRequirement
from app.core.scoring import score_profile_against_job
from app.core.transferable import TransferableSkillEngine
from app.core.reasoning_models import Phase2MatchResult, ReasoningTrace


class Phase2Evaluator:
    def __init__(self):
        print("🔧 Initializing Phase2Evaluator...")
        self.transfer_engine = TransferableSkillEngine()
        print("✅ Phase2Evaluator initialized successfully")

    def evaluate(
        self,
        profile: ProfessionalProfile,
        job: JobRequirement
    ) -> Phase2MatchResult:

        print(f"🚀 Starting Phase 2 evaluation for candidate: {profile.candidate_id}, job: {job.job_id}")
        
        print("📊 Step 1: Calculating baseline score...")
        baseline = score_profile_against_job(profile, job)
        print(f"✅ Baseline score: {baseline.fit_score}%")
        already_matched = set(s.lower() for s in baseline.breakdown.exact_skill_matches)

        print(f"🧠 Step 2: Inferring transferable skills...")
        print(f"   Candidate skills: {[s.name for s in profile.skills]}")
        print(f"   Job required skills: {job.required_skills}")
        
        transferable = self.transfer_engine.infer(
            candidate_skills=[s.name for s in profile.skills],
            job_skills=job.required_skills
        )
        # Filter out transferable skills that are the same as required skills
        original_count = len(transferable)
        # transferable = [
        #     inf for inf in transferable
        #     if inf.source_skill.lower() != inf.target_skill.lower()
        transferable = [
            inf for inf in transferable
            if inf.target_skill.lower() not in already_matched
        ]
        print(f"✅ Found {len(transferable)} transferable inferences (filtered from {original_count} total)")
        for i, inf in enumerate(transferable):
            print(f"   {i+1}. {inf.source_skill} → {inf.target_skill} (confidence: {inf.confidence})")

        print("⚖️ Step 3: Calculating score boost...")
        score_boost = sum(inf.confidence * 5 for inf in transferable)
        final_score = min(baseline.fit_score + score_boost, 100.0)
        print(f"   Score boost: {score_boost:.2f}")
        print(f"   Final score: {final_score:.2f}%")

        print("📝 Step 4: Building reasoning trace...")
        reasoning = ReasoningTrace(
            exact_matches=baseline.breakdown.exact_skill_matches,
            transferable_inferences=transferable,
            domain_signals=[],
            gaps=baseline.breakdown.missing_required_skills
        )
        print("✅ Reasoning trace built")

        result = Phase2MatchResult(
            candidate_id=profile.candidate_id,
            job_id=job.job_id,
            fit_score=round(final_score, 2),
            reasoning=reasoning
        )
        
        print(f"🎉 Phase 2 evaluation complete! Final score: {result.fit_score}%")
        return result
