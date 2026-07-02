import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import json

# Generate sample JIRA data for demonstration
def generate_sample_jira_data():
    np.random.seed(42)
    
    # Sample data for 6 months
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 6, 30)
    
    priorities = ['Critical', 'High', 'Medium', 'Low']
    statuses = ['Open', 'In Progress', 'Testing', 'Resolved', 'Closed']
    issue_types = ['Bug', 'Story', 'Task', 'Epic']
    components = ['Frontend', 'Backend', 'Database', 'API', 'Mobile']
    
    data = []
    for i in range(1000):
        created = start_date + timedelta(days=np.random.randint(0, 180))
        resolved = created + timedelta(days=np.random.randint(1, 30)) if np.random.random() > 0.3 else None
        
        data.append({
            'issue_key': f'PROJ-{i+1}',
            'priority': np.random.choice(priorities, p=[0.1, 0.3, 0.5, 0.1]),
            'status': np.random.choice(statuses, p=[0.1, 0.2, 0.15, 0.25, 0.3]),
            'issue_type': np.random.choice(issue_types, p=[0.4, 0.3, 0.2, 0.1]),
            'component': np.random.choice(components),
            'created_date': created,
            'resolved_date': resolved,
            'story_points': np.random.choice([1, 2, 3, 5, 8, 13], p=[0.2, 0.3, 0.25, 0.15, 0.08, 0.02]),
            'assignee': f'User{np.random.randint(1, 11)}'
        })
    
    return pd.DataFrame(data)

def create_visualizations():
    # Generate sample data
    df = generate_sample_jira_data()
    
    # Set style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # 1. Priority Distribution
    plt.figure(figsize=(10, 6))
    priority_counts = df['priority'].value_counts()
    colors = ['#ff4444', '#ff8800', '#ffcc00', '#44ff44']
    plt.pie(priority_counts.values, labels=priority_counts.index, autopct='%1.1f%%', colors=colors)
    plt.title('JIRA Issues by Priority Distribution', fontsize=16, fontweight='bold')
    plt.savefig('charts/priority_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Issues Created Over Time
    plt.figure(figsize=(12, 6))
    df['created_month'] = df['created_date'].dt.to_period('M')
    monthly_counts = df.groupby('created_month').size()
    monthly_counts.plot(kind='line', marker='o', linewidth=2, markersize=8)
    plt.title('Issues Created Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Number of Issues')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.savefig('charts/issues_over_time.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Resolution Time Analysis
    resolved_df = df[df['resolved_date'].notna()].copy()
    resolved_df['resolution_days'] = (resolved_df['resolved_date'] - resolved_df['created_date']).dt.days
    
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=resolved_df, x='priority', y='resolution_days')
    plt.title('Resolution Time by Priority', fontsize=16, fontweight='bold')
    plt.xlabel('Priority')
    plt.ylabel('Resolution Time (Days)')
    plt.savefig('charts/resolution_time.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Issue Type Distribution
    plt.figure(figsize=(10, 6))
    issue_type_counts = df['issue_type'].value_counts()
    bars = plt.bar(issue_type_counts.index, issue_type_counts.values, 
                   color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'])
    plt.title('Issues by Type', fontsize=16, fontweight='bold')
    plt.xlabel('Issue Type')
    plt.ylabel('Count')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.savefig('charts/issue_types.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Component Analysis
    plt.figure(figsize=(12, 8))
    component_priority = pd.crosstab(df['component'], df['priority'])
    component_priority.plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.title('Issues by Component and Priority', fontsize=16, fontweight='bold')
    plt.xlabel('Component')
    plt.ylabel('Number of Issues')
    plt.legend(title='Priority', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.savefig('charts/component_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Generate summary statistics
    stats = {
        'total_issues': len(df),
        'resolved_issues': len(resolved_df),
        'avg_resolution_time': resolved_df['resolution_days'].mean(),
        'critical_issues': len(df[df['priority'] == 'Critical']),
        'bug_percentage': (len(df[df['issue_type'] == 'Bug']) / len(df)) * 100
    }
    
    with open('data/summary_stats.json', 'w') as f:
        json.dump(stats, f, indent=2, default=str)
    
    print("✅ All visualizations created successfully!")
    return stats

if __name__ == "__main__":
    create_visualizations()