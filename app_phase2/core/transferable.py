import json
from typing import List
from app.core.llm_client import GeminiClient
from app.core.prompts import TRANSFERABLE_SKILL_PROMPT
from app.core.reasoning_models import TransferableSkillInference


class TransferableSkillEngine:
    def __init__(self):
        print("🤖 Initializing TransferableSkillEngine...")
        self.llm = GeminiClient()
        print("✅ TransferableSkillEngine initialized")

    def infer(
        self,
        candidate_skills: List[str],
        job_skills: List[str]
    ) -> List[TransferableSkillInference]:

        print("📝 Building transferable skills prompt...")
        prompt = TRANSFERABLE_SKILL_PROMPT.format(
            candidate_skills=candidate_skills,
            job_skills=job_skills
        )
        print(f"📋 Prompt length: {len(prompt)} characters")

        print("🔄 Calling LLM for transferable skills analysis...")
        raw = self.llm.generate(prompt)
        print(f"📤 LLM response length: {len(raw)} characters")
        print(f"📤 Raw response preview: {raw[:200]}...")
        
        # Check if response is truncated
        if len(raw) < 100:
            print("⚠️ Response seems very short, might be truncated")
        if not raw.strip().endswith(']') and not raw.strip().endswith('}'):
            print("⚠️ Response doesn't end with complete JSON")

        try:
            print("🔍 Parsing JSON response...")
            
            # Clean the response - remove markdown code blocks if present
            cleaned_raw = raw.strip()
            if cleaned_raw.startswith('```json'):
                cleaned_raw = cleaned_raw[7:]  # Remove ```json
            if cleaned_raw.startswith('```'):
                cleaned_raw = cleaned_raw[3:]   # Remove ```
            if cleaned_raw.endswith('```'):
                cleaned_raw = cleaned_raw[:-3]  # Remove trailing ```
            cleaned_raw = cleaned_raw.strip()
            
            print(f"🧹 Cleaned response preview: {cleaned_raw[:200]}...")
            
            # Try to fix incomplete JSON
            if not cleaned_raw.endswith(']') and not cleaned_raw.endswith('}'):
                print("🔧 Attempting to fix incomplete JSON...")
                
                # Find the last complete object and truncate there
                lines = cleaned_raw.split('\n')
                fixed_lines = []
                brace_count = 0
                bracket_count = 0
                in_string = False
                escape_next = False
                
                for line in lines:
                    line_fixed = line
                    for char in line:
                        if escape_next:
                            escape_next = False
                            continue
                        if char == '\\':
                            escape_next = True
                            continue
                        if char == '"' and not escape_next:
                            in_string = not in_string
                            continue
                        if not in_string:
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                            elif char == '[':
                                bracket_count += 1
                            elif char == ']':
                                bracket_count -= 1
                    
                    # Keep this line if we're still in a valid structure
                    if brace_count >= 0 and bracket_count >= 0:
                        fixed_lines.append(line)
                    else:
                        break
                
                cleaned_raw = '\n'.join(fixed_lines)
                
                # Close any remaining structures
                if brace_count > 0:
                    cleaned_raw += '\n' + '  ' * (brace_count - 1) + '}'
                if bracket_count > 0:
                    cleaned_raw += '\n]'
                    
                print(f"🔧 Fixed response preview: {cleaned_raw[:200]}...")
            
            parsed = json.loads(cleaned_raw)
            
            # Handle different response formats
            if isinstance(parsed, dict):
                if 'transferable_skills' in parsed:
                    inferences = parsed['transferable_skills']
                elif 'job_fit_assessment' in parsed and 'transferable_skills' in parsed['job_fit_assessment']:
                    inferences = parsed['job_fit_assessment']['transferable_skills']
                elif isinstance(parsed, list):
                    inferences = parsed
                else:
                    # Try to extract any list from the response
                    inferences = []
                    for key, value in parsed.items():
                        if isinstance(value, list):
                            inferences = value
                            break
            else:
                inferences = parsed
                
            result = [TransferableSkillInference(**p) for p in inferences]
            print(f"✅ Successfully parsed {len(result)} transferable inferences")
            for i, inf in enumerate(result):
                print(f"   {i+1}. {inf.source_skill} → {inf.target_skill} (confidence: {inf.confidence})")
            return result
        except Exception as e:
            print(f"❌ Failed to parse LLM response: {e}")
            print(f"   Raw response: {raw}")
            print(f"   Cleaned response: {cleaned_raw if 'cleaned_raw' in locals() else 'N/A'}")
            return []
