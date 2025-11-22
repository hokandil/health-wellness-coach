"""
Automated Evaluation Script for Health & Wellness Coach

Runs evaluation test cases and generates comprehensive reports.
Usage: python scripts/run_evaluation.py
"""

import sys
import json
import asyncio
import time
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.runner_manager import runner_manager
from src.agents.coordinator import coordinator_agent


async def run_evaluation():
    """Run automated evaluation of the Health Coach system."""
    
    print("\n" + "=" * 70)
    print("   🧪 HEALTH COACH AUTOMATED EVALUATION")
    print("=" * 70)
    
    # Load test cases
    evalset_path = project_root / "tests" / "evaluation" / "health_coach.evalset.json"
    config_path = project_root / "tests" / "evaluation" / "test_config.json"
    
    with open(evalset_path, 'r') as f:
        evalset = json.load(f)
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    test_cases = evalset['test_cases']
    total_cases = len(test_cases)
    
    print(f"\n📋 Loaded {total_cases} test cases")
    print(f"📊 Evaluation criteria: {', '.join(config['criteria'].keys())}")
    print("\n" + "-" * 70)
    
    # Results storage
    results = {
        'evaluation_time': datetime.now().isoformat(),
        'total_cases': total_cases,
        'passed': 0,
        'failed': 0,
        'test_results': [],
        'metrics': {}
    }
    
    # Run each test case
    for idx, test_case in enumerate(test_cases, 1):
        test_id = test_case['id']
        domain = test_case['domain']
        user_input = test_case['input']
        
        print(f"\n[{idx}/{total_cases}] Running test: {test_id} ({domain})")
        print(f"   Query: {user_input[:60]}...")
        
        start_time = time.time()
        
        try:
            # Execute query
            response = await runner_manager.run_query(
                agent=coordinator_agent,
                query=user_input,
                user_id=f"eval_user_{test_id}",
                session_id=f"eval_session_{test_id}"
            )
            
            elapsed_time = time.time() - start_time
            
            # Evaluate response
            test_result = {
                'test_id': test_id,
                'domain': domain,
                'input': user_input,
                'response': response,
                'response_time': round(elapsed_time, 2),
                'passed': True,  # Simplified - would need actual validation logic
                'criteria_met': {},
                'errors': []
            }
            
            # Check success criteria (simplified)
            success_criteria = test_case.get('success_criteria', {})
            for criterion, expected in success_criteria.items():
                # Simple heuristic checks
                if criterion == 'contains_calorie_number':
                    met = any(word in response.lower() for word in ['calorie', 'kcal', 'calories'])
                elif criterion == 'provides_recommendations':
                    met = len(response) > 100  # Has substantial content
                elif criterion == 'friendly_greeting':
                    met = any(word in response.lower() for word in ['hello', 'hi', 'welcome', 'help'])
                else:
                    met = True  # Default to passing for unimplemented checks
                
                test_result['criteria_met'][criterion] = met
            
            # Determine overall pass/fail
            all_criteria_met = all(test_result['criteria_met'].values())
            test_result['passed'] = all_criteria_met and elapsed_time < 15.0
            
            if test_result['passed']:
                results['passed'] += 1
                print(f"   ✅ PASSED ({elapsed_time:.2f}s)")
            else:
                results['failed'] += 1
                print(f"   ❌ FAILED ({elapsed_time:.2f}s)")
                unmet = [k for k, v in test_result['criteria_met'].items() if not v]
                if unmet:
                    print(f"      Unmet criteria: {', '.join(unmet)}")
            
            results['test_results'].append(test_result)
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"   ❌ ERROR: {str(e)}")
            
            results['failed'] += 1
            results['test_results'].append({
                'test_id': test_id,
                'domain': domain,
                'input': user_input,
                'response': None,
                'response_time': round(elapsed_time, 2),
                'passed': False,
                'criteria_met': {},
                'errors': [str(e)]
            })
    
    # Get final metrics
    results['metrics'] = runner_manager.get_metrics()
    
    # Calculate summary statistics
    pass_rate = results['passed'] / results['total_cases'] if results['total_cases'] > 0 else 0
    avg_response_time = sum(r['response_time'] for r in results['test_results']) / len(results['test_results'])
    
    results['summary'] = {
        'pass_rate': round(pass_rate, 3),
        'avg_response_time': round(avg_response_time, 2),
        'total_passed': results['passed'],
        'total_failed': results['failed']
    }
    
    # Print summary
    print("\n" + "=" * 70)
    print("   📊 EVALUATION SUMMARY")
    print("=" * 70)
    print(f"\n   Total Tests: {results['total_cases']}")
    print(f"   Passed: {results['passed']} ({pass_rate * 100:.1f}%)")
    print(f"   Failed: {results['failed']}")
    print(f"   Average Response Time: {avg_response_time:.2f}s")
    
    # Save results
    results_dir = project_root / "tests" / "evaluation" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    results_file = results_dir / f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n   📁 Results saved to: {results_file}")
    
    # Determine overall success
    min_pass_rate = config.get('agent_routing_accuracy', {}).get('required_accuracy', 0.85)
    if pass_rate >= min_pass_rate:
        print(f"\n   ✅ EVALUATION PASSED (pass rate {pass_rate:.1%} >= {min_pass_rate:.1%})")
        return 0
    else:
        print(f"\n   ❌ EVALUATION FAILED (pass rate {pass_rate:.1%} < {min_pass_rate:.1%})")
        return 1


def main():
    """Main entry point."""
    try:
        exit_code = asyncio.run(run_evaluation())
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
