"""
Show Cause Notice Generator - Generates regulatory notices from gap analysis results.
"""
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import os
from typing import Dict, List, Optional


def generate_notice(gap_result: Dict) -> str:
    """
    Generate a show cause notice from gap analysis result.
    
    Args:
        gap_result: Dictionary containing gap analysis data
        
    Returns:
        Formatted notice string
    """
    product_name = gap_result.get('product_name', 'Unknown Product')
    risk_level = gap_result.get('risk_level', 'medium').upper()
    risk_score = gap_result.get('overall_risk_score', 0.5)
    dissatisfaction = gap_result.get('dissatisfaction_index', 0)
    
    notice = f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║              SHOW CAUSE NOTICE - REGULATORY ALERT             ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    Date: {datetime.now().strftime('%Y-%m-%d')}
    Time: {datetime.now().strftime('%H:%M:%S')}
    
    To: {product_name}
    From: SEBI / RBI Regulatory Authority
    Subject: Mis-selling Violations Detected - Immediate Action Required
    
    ════════════════════════════════════════════════════════════════
    RISK ASSESSMENT
    ════════════════════════════════════════════════════════════════
    Risk Level: {risk_level}
    Risk Score: {risk_score:.2f}/1.0
    Customer Dissatisfaction Index: {dissatisfaction:.1f}%
    
    ════════════════════════════════════════════════════════════════
    DETECTED VIOLATIONS
    ════════════════════════════════════════════════════════════════
    """
    
    # Extract mismatches
    mismatches = []
    try:
        if isinstance(gap_result.get('mismatches'), str):
            mismatches = json.loads(gap_result.get('mismatches', '[]'))
        elif isinstance(gap_result.get('mismatches'), list):
            mismatches = gap_result.get('mismatches', [])
    except:
        pass
    
    if mismatches:
        for i, mismatch in enumerate(mismatches[:5], 1):  # Limit to top 5
            aspect = mismatch.get('promise_aspect', 'Unknown')
            topic = mismatch.get('complaint_topic', 'General complaint')
            severity = mismatch.get('severity', 0.5)
            mismatch_type = mismatch.get('mismatch_type', 'direct_contradiction')
            
            notice += f"""
    {i}. VIOLATION: {aspect}
       Issue: {topic}
       Severity: {severity:.2f}/1.0
       Type: {mismatch_type.replace('_', ' ').title()}
       """
            
            # Add evidence if available
            evidence = mismatch.get('evidence', [])
            if evidence:
                notice += "   Evidence:\n"
                for ev in evidence[:2]:  # Limit to 2 pieces of evidence
                    notice += f"      - {ev}\n"
    else:
        notice += """
    General mis-selling concerns detected based on customer sentiment analysis.
    """
    
    notice += f"""
    ════════════════════════════════════════════════════════════════
    RECOMMENDED ACTIONS
    ════════════════════════════════════════════════════════════════
    """
    
    # Add recommendations
    recommendations = []
    try:
        if isinstance(gap_result.get('recommendations'), str):
            recommendations = json.loads(gap_result.get('recommendations', '[]'))
        elif isinstance(gap_result.get('recommendations'), list):
            recommendations = gap_result.get('recommendations', [])
    except:
        pass
    
    if recommendations:
        for i, rec in enumerate(recommendations[:5], 1):
            notice += f"    {i}. {rec}\n"
    else:
        notice += """    1. Immediate investigation required
    2. Review product disclosures and marketing materials
    3. Address customer complaints promptly
    4. Provide detailed response within 7 days
    5. Implement corrective measures
    """
    
    notice += f"""
    ════════════════════════════════════════════════════════════════
    RESPONSE REQUIRED
    ════════════════════════════════════════════════════════════════
    
    You are required to respond to this notice within 7 (seven) days
    from the date of issue, providing:
    
    1. Detailed explanation of the detected discrepancies
    2. Corrective actions taken or proposed
    3. Evidence of compliance improvements
    4. Customer compensation plan (if applicable)
    
    Failure to respond may result in regulatory action including:
    - Suspension of product sales
    - Monetary penalties
    - License revocation
    
    ════════════════════════════════════════════════════════════════
    
    This notice is generated automatically by Veritas Finance
    AI-Powered Mis-selling Detection System.
    
    For queries, contact: regulatory@veritasfinance.ai
    """
    
    return notice


def generate_notices_from_csv(csv_path: str = "data/processed/gap_analysis.csv", 
                              output_dir: str = "reports/notices") -> List[str]:
    """
    Generate notices for all products in gap analysis CSV.
    
    Args:
        csv_path: Path to gap analysis CSV file
        output_dir: Directory to save notice files
        
    Returns:
        List of generated notice file paths
    """
    if not os.path.exists(csv_path):
        print(f"❌ Gap analysis file not found: {csv_path}")
        print("💡 Run: python main_pipeline.py")
        return []
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load gap analysis
    try:
        gap_df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return []
    
    generated_files = []
    
    print("=" * 60)
    print("GENERATING SHOW CAUSE NOTICES")
    print("=" * 60)
    
    for _, row in gap_df.iterrows():
        product_name = row.get('product_name', 'Unknown')
        risk_level = str(row.get('risk_level', 'medium')).lower()
        
        # Only generate notices for high/critical risk products
        if risk_level in ['high', 'critical']:
            notice = generate_notice(row.to_dict())
            
            # Save to file
            safe_filename = product_name.replace(' ', '_').replace('/', '_')
            notice_path = os.path.join(output_dir, f"{safe_filename}_notice.txt")
            
            with open(notice_path, 'w', encoding='utf-8') as f:
                f.write(notice)
            
            generated_files.append(notice_path)
            print(f"✅ Generated notice for: {product_name} ({risk_level.upper()})")
            print(f"   Saved to: {notice_path}")
    
    if not generated_files:
        print("ℹ️ No high-risk products found. No notices generated.")
    
    print(f"\n✅ Generated {len(generated_files)} notice(s)")
    return generated_files


if __name__ == "__main__":
    print("=" * 60)
    print("SHOW CAUSE NOTICE GENERATOR")
    print("=" * 60)
    print()
    
    # Generate notices
    notices = generate_notices_from_csv()
    
    if notices:
        print("\n📋 Sample Notice Preview:")
        print("=" * 60)
        with open(notices[0], 'r', encoding='utf-8') as f:
            print(f.read()[:500] + "...")
    else:
        print("\n💡 To generate notices:")
        print("   1. Run: python mock_data_generator.py")
        print("   2. Run: python main_pipeline.py")
        print("   3. Run: python features/notice_generator.py")
